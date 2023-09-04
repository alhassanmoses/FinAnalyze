from transaction.schemas import (
    CreateTransaction,
    TransactionGetResponse,
    TransactionUpdate,
)
from transaction.data_util import (
    validate_record,
    retrieve_record,
    get_records,
    update_record,
    remove_record,
    get_analytics,
)
from dependencies.sharedutils.jsonencoder import jsonHelper
from dependencies.sharedutils.api_messages import gettext
from dependencies.sharedutils.db import get_database
from core_service.exceptions import CurrentUserNotFound, NoneOwnerPermissionDenied
from auth.schema import User

from fastapi import APIRouter, status, Depends, Request, Body, Path
from fastapi.responses import JSONResponse
from bson.codec_options import TypeCodec, TypeRegistry
from bson.decimal128 import Decimal128
from typing import List, Optional, Dict
from decimal import Decimal
from motor.motor_asyncio import AsyncIOMotorClient

transaction_router = APIRouter(
    prefix="/transaction",
    tags=["Transaction"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Resource Not found"}},
)


class Decimal128Converter(TypeCodec):
    """
    A custom converter Decimal128Converter to handle the
    transformation between Decimal and Decimal128 types.

    """

    python_type = Decimal
    bson_type = Decimal128  # A safe floating point type provide by mongodb to handle manupulation of sensitive financial decimal values.

    def transform_bson(self, value, codec_options):
        return Decimal(value.to_decimal())

    def transform_python(self, value):
        return Decimal128(value)


# Resgistering the converter in the TypeRegistry
# and setting the codec_options accordingly.
registry = TypeRegistry([Decimal128Converter()])
codec_options = codec_options = TypeRegistry([Decimal128Converter()])


@transaction_router.post(
    "/create",
    response_model=TransactionGetResponse,
    summary="Creates a transaction record.",
)
async def create_transaction(
    request: Request,
    db: AsyncIOMotorClient = Depends(get_database),
    transaction_record: CreateTransaction = Body(...),
):
    user_id = request.app.current_user_id
    if user_id is None:
        raise CurrentUserNotFound

    record: dict = await validate_record(user_id, transaction_record, db)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonHelper(record))


@transaction_router.get(
    "/all",
    response_model=List[TransactionGetResponse],
    summary="Retrieve a transaction record for a given record_id.",
)
async def get_transactions(
    request: Request,
    db: AsyncIOMotorClient = Depends(get_database),
):
    current_user_id = request.app.current_user_id

    records = await get_records(current_user_id, db)

    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonHelper(records))


@transaction_router.put(
    "/update/{record_id:str}",
    response_model=TransactionGetResponse,
    summary="Creates a transaction record.",
)
async def update_transaction(
    request: Request,
    db: AsyncIOMotorClient = Depends(get_database),
    record_id: str = Path(..., description="The ID of the record to be updated."),
    new_record: TransactionUpdate = Body(...),
):
    user_id = request.app.current_user_id
    if user_id is None:
        raise CurrentUserNotFound

    old_record: dict = await retrieve_record(record_id, db)

    updated_record: dict = await update_record(record_id, new_record, old_record, db)

    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED, content=jsonHelper(updated_record)
    )


@transaction_router.delete(
    "/delete/{record_id:str}",
    response_model=TransactionGetResponse,
    summary="Removes a transaction record.",
)
async def delete_transaction(
    request: Request,
    db: AsyncIOMotorClient = Depends(get_database),
    record_id: str = Path(..., description="The ID of the record to be updated."),
):
    # TODO: Abstruct this initial repeating logic to a helper middleware
    user_id = request.app.current_user_id
    if user_id is None:
        raise CurrentUserNotFound

    record: Optional[dict] = TransactionGetResponse.get_by_id(
        record_id, "transactions", db
    )

    success = await remove_record(record_id, db, soft_delete=False)

    if success:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"message": "success"}
        )


@transaction_router.get(
    "/analytics/{user_id:str}",
    summary="Analyses a users records to provides userful insights.",
)
async def analyse_records(
    request: Request,
    db: AsyncIOMotorClient = Depends(get_database),
    user_id: str = Path(
        ..., description="The ID of the user who's records are to be analysed."
    ),
):
    current_user_id = request.app.current_user_id

    if user_id is None:
        raise CurrentUserNotFound
    if user_id != current_user_id:
        raise NoneOwnerPermissionDenied(
            status_code=status.HTTP_RESOURCE_REQUEST,
            detail=gettext("INVALID_RESOURCE_REQUEST"),
        )

    records: List[Dict[str, any]] = await get_analytics(user_id, db)

    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonHelper(records))


@transaction_router.get(
    "/{record_id:str}",
    response_model=TransactionGetResponse,
    summary="Retrieve a transaction record for a given record_id.",
)
async def get_transaction(
    db: AsyncIOMotorClient = Depends(get_database),
    record_id: str = Path(
        ..., title="The Transaction Record ID for the record to be retrieved"
    ),
):
    record: dict = await retrieve_record(record_id, db)

    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonHelper(record))
