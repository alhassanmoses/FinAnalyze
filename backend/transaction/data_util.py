from motor.core import AgnosticDatabase
from transaction.schemas import CreateTransaction, Transaction
from auth.schema import User
from fastapi import HTTPException, status
from fastapi.exceptions import RequestValidationError
from bson import Decimal128


async def validate_record(
    user_id: str, transaction: CreateTransaction, db: AgnosticDatabase
) -> Transaction:
    try:
        user = await User.get_by_id(user_id, "users", db)
        if not user:
            raise RequestValidationError(
                "Invalid request, the user issuing this trasaction does not exist on this platform."
            )
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
    record: Transaction = Transaction(**record)

    if record is None:
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Failed to save the record to the database.",
        )

    return record
