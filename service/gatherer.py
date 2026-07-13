import requests
from model.constants import EXCHANGE_RATE_API_SOURCE
import service.response_transformers as response_transformers
import datetime
from env_manager import get_env_variable

from db.database import (
    upsert_currency_rates
)


gathering_jobs = [
    {
        "name": "Currency rates from {}".format(EXCHANGE_RATE_API_SOURCE),
        "url": 'https://v6.exchangerate-api.com/v6/{}/latest/USD'.format(get_env_variable("EXCHANGE_RATE_API_KEY")),
        "transformer": response_transformers.tranform_exchange_rate_api_response,
        "run_times_per_day": 3,
    }
]

def start_gathering_job(job: dict):
    print(datetime.datetime.now(), ' Starting the job: {}...'.format(job["name"]))
    
    if job:
        response = requests.get(job["url"])

        print(datetime.datetime.now(), "[", job["name"], "] Response: ", response)

        if response.ok:
            parsed_rates_list = job["transformer"](response.json())
            upsert_currency_rates(parsed_rates_list)
    
    print(datetime.datetime.now(), ' Finishing the job: {}...'.format(job["name"]))