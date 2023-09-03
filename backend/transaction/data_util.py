import logging
from datetime import datetime

from cachetools import TTLCache, cached
from motor.core import AgnosticDatabase
from fastapi import HTTPException, status
from fastapi.exceptions import RequestValidationError
from bson import Decimal128, ObjectId

from transaction.schemas import CreateTransaction, Transaction, TransactionUpdate
from auth.schema import User
from dependencies.sharedutils.api_messages import gettext
from typing import Dict, List


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

    try:
        updated_record = await db.transactions.update_one(
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


# Create a cache with a maximum size and time-based expiration
cache = TTLCache(maxsize=100, ttl=60)


def fetch_data():
    return {"data": "Get analytic data"}


# Use the cached decorator to cache the response
@cached(cache)
def get_analytics():
    return fetch_data()
