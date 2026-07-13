import requests
from model.constants import EXCHANGE_RATE_API_SOURCE
import service.response_transformers as response_transformers
import datetime
from env_manager import get_env_variable

from db.database import (
    upsert_currency_rates
)


gatherers = {
    "exchange_rate_api": {
        "name": EXCHANGE_RATE_API_SOURCE,
        "url": 'https://v6.exchangerate-api.com/v6/{}/latest/USD'.format(get_env_variable("EXCHANGE_RATE_API_KEY")),
        "transformer": response_transformers.tranform_exchange_rate_api_response,
    }
}

default_gatherer_id = "exchange_rate_api"


def gather_currency_rates():
    print(datetime.datetime.now(), ' Currency rates refreshing started')
    gatherer = gatherers[default_gatherer_id]

    if gatherer:
        print(datetime.datetime.now(), ' Getting data by url')
        response = requests.get(gatherer["url"])

        if response.ok:
            parsed_rates_list = gatherer["transformer"](response.json())
            upsert_currency_rates(parsed_rates_list)
    
    print(datetime.datetime.now(), ' Currency rates refreshing finished')


