from model.constants import EXCHANGE_RATE_API_SOURCE

def tranform_exchange_rate_api_response(json_response: dict) -> list:
    return [
        {
            "source": EXCHANGE_RATE_API_SOURCE,
            "rates": {k : (1 / v) for k,v in json_response['conversion_rates'].items()}
        }
    ]