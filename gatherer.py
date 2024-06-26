import requests
import response_transformers
import datetime
from env_manager import get_env_variable

from database import (
    upsert_currency_rates
)


gatherers = {
    "exchange_rate_api": {
        "url": 'https://v6.exchangerate-api.com/v6/{}/latest/USD'.format(get_env_variable("EXCHANGE_RATE_API_KEY")),
        "transformer": response_transformers.tranform_exchange_rate_api_response,
    }
}

default_gatherer_id = "exchange_rate_api"


def gather_currency_rates():
    print(datetime.datetime.now(), ' Refresh currency rates started')
    gatherer = gatherers[default_gatherer_id]

    if gatherer:
        print(datetime.datetime.now(), ' Getting data by url')
        response = requests.get(gatherer["url"])

        if response.ok:
            result = gatherer["transformer"](response.json())
            upsert_currency_rates(result)
    
    print(datetime.datetime.now(), ' Refresh currency rates finished')


