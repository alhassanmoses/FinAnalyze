from fastapi import APIRouter, status, Depends, Request
from fastapi.responses import JSONResponse
from transaction.schemas import Transaction, CreateTransaction, TransactionResponse
from transaction.data_util import validate_record
from bson.codec_options import TypeCodec, TypeRegistry
from bson.decimal128 import Decimal128
from decimal import Decimal
from dependencies.sharedutils.jsonencoder import jsonHelper, JSONEncoder
from fastapi.encoders import jsonable_encoder


transaction_router = APIRouter(
    prefix="/transaction",
    tags=["Transaction"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Resource Not found"}},
)


@transaction_router.get("/home", summary="Generate a User token.")
async def go_home():
    return "Json"


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
    "/", response_model=TransactionResponse, summary="Creates a transaction record."
)
async def create_transaction(
    request: Request,
    transaction_record: CreateTransaction = Depends(),
):
    user_id = request.app.current_user_id
    db = request.app.db
    # if user_id != transaction_record.user.id

    record: Transaction = await validate_record(user_id, transaction_record, db)

    return jsonHelper(record.dict())
