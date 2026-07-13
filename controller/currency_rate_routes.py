from fastapi import APIRouter, Body
from typing import Annotated
from model.constants import EXCHANGE_RATE_API_SOURCE
import service.util as util

from db.database import (
    retrieve_currency_rates,
    retrieve_currency_rates_sources,
    retrieve_currency_rate,
    upsert_currency_rates
)

currency_rate_router = APIRouter()


@currency_rate_router.get("/", response_description = "Get all exchange rates")
async def get_currency_rates(source: str = EXCHANGE_RATE_API_SOURCE):
    return await retrieve_currency_rates(source)

@currency_rate_router.get("/sources", response_description = "Get all exchange rates sources (API and banks)")
async def get_currency_rates_sources():
    return await retrieve_currency_rates_sources()

@currency_rate_router.get("/{code}", response_description = "Get exchange rate by currency code")
async def get_currency_rate_data(code: str, source: str = EXCHANGE_RATE_API_SOURCE):
    return await retrieve_currency_rate(source, code.upper())


@currency_rate_router.post("/", response_description = "Add exchange rates")
async def upsert_currency_rates_data(currency_rates: Annotated[
        list,
        Body(
            examples=[
                {
                    "source": "testSource",
                    "rates": {
                        "USD": 1,
                        "EUR": 1.2
                    }
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