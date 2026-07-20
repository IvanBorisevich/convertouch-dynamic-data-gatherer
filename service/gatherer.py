import requests
from model.constants import COIN_GECKO_API_SOURCE, CURRENCY_RATES_DATA_TYPE, EXCHANGE_RATE_API_SOURCE, FLOAT_RATES_API_SOURCE
import service.response_parsers as response_parsers
import datetime
from env_manager import get_env_variable

from db.database import (
    upsert_currency_rates
)


gathering_jobs = [
    {
        "source_name": EXCHANGE_RATE_API_SOURCE,
        "url": 'https://v6.exchangerate-api.com/v6/{}/latest/USD'.format(get_env_variable("EXCHANGE_RATE_API_KEY")),
        "transformer": response_parsers.parse_exchange_rate_response,
        "run_times_per_day": 3,
        "delay_before_start_in_sec": 0,
        "data_type": CURRENCY_RATES_DATA_TYPE
    },
    {
        "source_name": FLOAT_RATES_API_SOURCE,
        "url": 'https://www.floatrates.com/daily/usd.json',
        "transformer": response_parsers.parse_float_rates_response,
        "run_times_per_day": 3,
        "delay_before_start_in_sec": 10 * 60,
        "data_type": CURRENCY_RATES_DATA_TYPE
    },
    {
        "source_name": COIN_GECKO_API_SOURCE,
        "url": 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd',
        "transformer": response_parsers.parse_coin_gecko_response,
        "run_times_per_day": 3,
        "delay_before_start_in_sec": 10 * 60,
        "data_type": CURRENCY_RATES_DATA_TYPE
    }
]

def start_gathering_job(job: dict):
    job_name = '{} from {}'.format(job['data_type'], job['source_name'])

    print(datetime.datetime.now(), "[ {} ] Starting the job ...".format(job_name))
    
    if job:
        response = requests.get(job["url"])

        print(datetime.datetime.now(), "[ {} ] Job response: {}".format(job_name, response))

        if response.ok:
            parsed_rates_list = job["transformer"](response.json())
            upsert_currency_rates(parsed_rates_list)
    
    print(datetime.datetime.now(), "[ {} ] The job has been finished!".format(job_name))