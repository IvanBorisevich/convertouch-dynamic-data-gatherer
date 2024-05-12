from fastapi import APIRouter, Body
from typing import Annotated
import util

from database import (
    retrieve_currency_rates,
    retrieve_currency_rate,
    upsert_currency_rates
)

router = APIRouter()


@router.get("/", response_description = "Get all exchange rates")
async def get_currency_rates():
    return await retrieve_currency_rates()


@router.get("/{code}", response_description = "Get exchange rate by currency code")
async def get_currency_rate_data(code: str):
    return await retrieve_currency_rate(code.upper())


@router.post("/", response_description = "Add exchange rates")
async def upsert_currency_rates_data(currency_rates: Annotated[
        dict,
        Body(
            examples=[
                {
                    "USD": 1,
                    "EUR": 1.2
                }
            ],
        ),
    ]):
    try:
        upsert_currency_rates(currency_rates)
    except Exception as e:
        print("Error during upsert: ", util.format_exception(e))
        return {"result": e.message if hasattr(e, 'message') else str(e)}
    else:
        return {"result": "OK"}