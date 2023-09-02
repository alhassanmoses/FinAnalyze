from fastapi import APIRouter, status, Depends, Request

# from auth.data_util import get_current_user

transaction_router = APIRouter(
    prefix="/transaction",
    tags=["Transaction"],
    # dependencies=[
    #     Depends(get_current_user)
    # ],  # Moved dependencies to super router object
    responses={status.HTTP_404_NOT_FOUND: {"description": "Resource Not found"}},
)


# @transaction_router.get("lalaland/")
# def get_some():
#     return "Something spicy"
@transaction_router.get("/home", summary="Generate a User token.")
async def go_home():
    return "Json"
