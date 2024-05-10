import requests
import response_transformers
from dotenv import dotenv_values
import datetime

from database import (
    upsert_currency_rates
)

config = dotenv_values(".env")

gatherers = {
    "exchange_rate_api": {
        "url": 'https://v6.exchangerate-api.com/v6/{}/latest/USD'.format(config["EXCHANGE_RATE_API_KEY"]),
        "transformer": response_transformers.tranform_exchange_rate_api_response,
    }
}

default_gatherer_id = "exchange_rate_api"


async def gather_currency_rates():
    print(datetime.datetime.now(), ' Refresh currency rates started')
    gatherer = gatherers[default_gatherer_id]

    if gatherer:
        print(datetime.datetime.now(), ' Getting data by url')
        response = requests.get(gatherer["url"])

        if response.ok:
            result = gatherer["transformer"](response.json())
            await upsert_currency_rates(result)
    
    print(datetime.datetime.now(), ' Refresh currency rates finished')





