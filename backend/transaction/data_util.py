import logging
from datetime import datetime

from motor.core import AgnosticDatabase
from fastapi import HTTPException, status
from fastapi.exceptions import RequestValidationError
from bson import Decimal128, ObjectId
from decimal import Decimal

from transaction.schemas import CreateTransaction, Transaction, TransactionUpdate
from dependencies.sharedutils.db import get_base_query
from dependencies.sharedutils.api_messages import gettext
from auth.schema import User
from typing import Dict, List, Optional
from cachetools import TTLCache, cached


def format_record(record):
    # Shallow Soft delete implementation
    if record.get("_deleted", None) != None:
        return {}

    response = {
        "_id": record.get("_id"),
        "user_id": record.get("user")["_id"],
        "transaction_type": record.get("transaction_type"),
        "status": record.get("status"),
        "amount": record.get("amount"),
        "currency": record.get("currency"),
        "display_amount": record.get("display_amount"),
        "created": record.get("created"),
        "last_modified": record.get("last_modified"),
    }

    return response


async def validate_record(
    user_id: str, transaction: CreateTransaction, db: AgnosticDatabase
) -> dict:
    try:
        user = await User.get_by_id(user_id, "users", db)
        if not user:
            raise RequestValidationError(gettext("TRANSACTION_WITH_INVALID_USER_ID"))
        result = await db.transactions.insert_one(
            {
                **transaction.to_dict(),
                "amount": Decimal128(
                    transaction.amount
                ),  # overriding and saving amount as a Decimal128 object in mongodb to prevent float approximation
                **get_base_query(is_insert=True),
                "user": user,
            }
        )
        record_id = result.inserted_id

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

    record: dict = await Transaction.get_by_id(record_id, "transactions", db)
    record: dict = format_record(record)

    if record is None:
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail=gettext("FAILED_DB_PERSIST"),
        )

    return record


async def retrieve_record(record_id: str, db: AgnosticDatabase):
    record = await Transaction.get_by_id(record_id, "transactions", db)

    return format_record(record)


async def get_records(
    current_user_id: str, db: AgnosticDatabase
) -> List[Dict[str, any]]:
    cursor = db.transactions.find({"user._id": ObjectId(current_user_id)})
    records = await cursor.to_list(length=None)
    records_list = [format_record(record) for record in records]

    return records_list


async def update_record(record_id, new_record: TransactionUpdate, old_record, db):
    updates = {key: value for key, value in new_record.dict().items() if value}
    updates.update(get_base_query(is_update=True))

    try:
        await db.transactions.update_one(
            {"_id": ObjectId(record_id)}, {"$set": updates}
        )
    except Exception as e:
        logging.error(
            f"Failed to update record({record_id}) with {updates}. Error:\n{e}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

    record: dict = await Transaction.get_by_id(record_id, "transactions", db)
    record: dict = format_record(record)

    return record


async def remove_record(record_id: str, db: AgnosticDatabase, soft_delete: bool = True):
    try:
        if soft_delete:
            await db.transactions.find_one_and_update(
                {"_id": ObjectId(record_id)}, {"$set": {"_deleted": datetime.utcnow()}}
            )
            return True
        await db.transactions.find_one_and_delete({"_id": ObjectId(record_id)})
        return True

    except Exception as e:
        logging.error(
            f"Error while {'soft' if soft_delete else 'hard'} deleting Transaction record with ID({record_id})."
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete Transaction record with ID({record_id}).",
        )


# Creates a cache with a maximum size and time-based expiration
cache = TTLCache(maxsize=100, ttl=1)


@cached(cache)
async def generate_analytics(user_id: str, db: AgnosticDatabase):
    # Check the cache first
    cached_response = cache.get(user_id)
    if cached_response:
        return cached_response

    cursor = db.transactions.find({"user._id": ObjectId(user_id)})

    total_amount: Decimal = Decimal("0")
    daily_transaction_count: Dict[datetime.date, int] = {}
    user_transactions = await cursor.to_list(length=None)
    for transaction in user_transactions:
        # Convert Decimal128 to Decimal for addition
        transaction_amount: Decimal = Decimal(transaction["amount"].to_decimal())

        # Calculating total transaction amount
        total_amount += transaction_amount

        # Extracting transaction date to get the day (ignoring time)
        transaction_date: datetime.date = transaction["created"].date()

        # Updating transaction count of the processed date
        daily_transaction_count[transaction_date] = (
            daily_transaction_count.get(transaction_date, 0) + 1
        )

    # Calculating the average transaction value
    num_transactions: int = len(user_transactions)
    if num_transactions == 0:
        average_transaction_value: Decimal = Decimal("0")
    else:
        average_transaction_value: Decimal = total_amount / Decimal(
            str(num_transactions)
        )

    # Finding the day with the highest number of transactions
    if daily_transaction_count:
        max_transaction_day: datetime.date = max(
            daily_transaction_count, key=daily_transaction_count.get
        )
    else:
        max_transaction_day: Optional[datetime.date] = None

    response_data: Dict[str, str] = {
        "user_id": user_id,
        "average_transaction_value": str(average_transaction_value),
        "day_with_highest_transactions": str(max_transaction_day),
    }

    cache[user_id] = response_data

    return response_data


async def get_analytics(user_id: str, db: AgnosticDatabase):
    return await generate_analytics(user_id, db)
