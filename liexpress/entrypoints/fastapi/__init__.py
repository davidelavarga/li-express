import logging
import os
from http import HTTPStatus
from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request, Security, status
from fastapi.openapi.models import APIKey
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader

from liexpress.bootstrap import configure_inject

app = FastAPI(root_path=os.getenv("ROOT_PATH", ""))

# Security
__API_KEYS = os.getenv("API_KEYS", "").split(",")
auth_header = APIKeyHeader(name="Authorization")


async def verify_api_key(api_key_header: str = Security(auth_header)):
    if api_key_header not in __API_KEYS:
        logging.error(f"Bad API key: {api_key_header}")
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED.value,
            detail=f"{HTTPStatus.UNAUTHORIZED.name}. Bad API key provided",
        )


@app.on_event("startup")
async def startup_event():
    configure_inject()


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
        content={
            "status": f"{HTTPStatus.INTERNAL_SERVER_ERROR.name}",
            "ErrorMessage": f"{exc}",
        },
    )
