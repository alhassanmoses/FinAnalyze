import logging

from main import app

from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import Request, status, HTTPException
from dependencies.sharedutils.api_messages import gettext


# TODO: Move all logs from out stream and write them to a filestream
# Included a logging side effect to all exceptions
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logging.exception(
        f"Validation exception(s).\nstatus returned: {exc.status_code}\ndetails: {exc.errors()}\bbody:{exc.body}"
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({"details": exc.errors(), "body": exc.body}),
    )


# Custom exception handler for validation errors
@app.exception_handler(HTTPException)
async def validation_exception_handler(request, exc):
    logging.exception(
        f"HTTP exception.\nstatus returned: {exc.status_code}\ndetails: {exc.errors()}\bbody:{exc.body}"
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logging.exception(
        f"Generic exception.\nstatus returned: {exc.status_code}\ndetails: {exc.errors()}\bbody:{exc.body}"
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": gettext("UNKNOWN_EXCEPTION")},
    )
