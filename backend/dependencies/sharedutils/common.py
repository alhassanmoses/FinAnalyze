from jose import jwt
from typing import Dict

from fastapi import Depends, HTTPException, Header, status


from dependencies.settings import settings


# TODO: Might switch to this later
# async def get_token_header(x_token: str = Header('X-finanalyze')):
#     if x_token != "===":
#         raise HTTPException(status_code=400, detail="X-finanalyze header Invalid")
