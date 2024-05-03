from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from database import (
    retrieve_currency_rates,
    add_currency_rate,
    retrieve_currency_rate
)
from models import (
    CurrencyRate,
    CurrencyRateUpdate,
    ErrorResponseModel,
    ResponseModel
)

router = APIRouter()


@router.get("/", response_description="currency_rates retrieved")
async def get_currency_rates():
    currency_rates = await retrieve_currency_rates()
    if currency_rates:
        return ResponseModel(currency_rates, "currency_rates data retrieved successfully")
    return ResponseModel(currency_rates, "Empty list returned")


@router.get("/{id}", response_description="currency_rate data retrieved")
async def get_currency_rate_data(id):
    currency_rate = await retrieve_currency_rate(id)
    if currency_rate:
        return ResponseModel(currency_rate, "currency_rate data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "currency_rate doesn't exist.")