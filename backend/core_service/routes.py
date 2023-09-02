from fastapi import APIRouter
from auth.auth_api import user_router
from transaction.transaction_api import transaction_router

router = APIRouter()

router.include_router(transaction_router)
router.include_router(user_router)
