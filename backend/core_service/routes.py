from fastapi import APIRouter, Depends

from auth.auth_api import user_router
from auth.data_util import get_current_user
from transaction.transaction_api import transaction_router

router = APIRouter()
router.include_router(transaction_router, dependencies=[Depends(get_current_user)])
router.include_router(user_router)
