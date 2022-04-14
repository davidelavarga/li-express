import logging
import os
from http import HTTPStatus
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query, Request, Security, status
from fastapi.openapi.models import APIKey
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader

from liexpress.bootstrap import configure_inject
from liexpress.domain.actions.product_detail import ProductDetail
from liexpress.domain.actions.products_list import ProductList
from liexpress.domain.models.exceptions import InputException
from liexpress.entrypoints.fastapi.models import (
    Configuration,
    DetailProductResponse,
    PlainProductResponse,
)

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


@app.exception_handler(InputException)
async def input_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=HTTPStatus.BAD_REQUEST.value,
        content={
            "status": f"{HTTPStatus.BAD_REQUEST.name}",
            "ErrorMessage": f"{exc}",
        },
    )


@app.get(
    "/reservation/{reservation_id}/products/",
    response_model=List[PlainProductResponse],
    status_code=status.HTTP_200_OK,
    summary="Get products for the given reservation_id",
)
async def get_products(
    reservation_id: int,
    relevance: str = Query(..., description="Ways to order the products"),
    active_products: Optional[bool] = Query(
        True,
        description=" If active=true return only active product, return all products otherwise",
    ),
    api_key: APIKey = Depends(verify_api_key),
):
    products = ProductList()(reservation_id, relevance, active_products)
    return [
        PlainProductResponse(
            product_id=p.product_id,
            name=p.name.capitalize(),
            description=p.description,
            date_added=p.date_added,
            price=p.price,
        )
        for p in products
    ]


@app.get(
    "/reservation/{reservation_id}/products/{product_id}",
    response_model=DetailProductResponse,
    status_code=status.HTTP_200_OK,
    summary="Get product detail for the given reservation_id, including place holders",
)
async def get_product_detal(
    reservation_id: int,
    product_id: int,
    api_key: APIKey = Depends(verify_api_key),
):
    p = ProductDetail()(reservation_id, product_id)

    return DetailProductResponse(
        product_id=p.product_id,
        name=p.name.capitalize(),
        description=p.description,
        date_added=p.date_added,
        price=p.price,
        order_fields=[
            Configuration(name=c.name, type=c.type) for c in p.configurations
        ],
    )
