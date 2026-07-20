from model.constants import COIN_GECKO_API_SOURCE, EXCHANGE_RATE_API_SOURCE, FLOAT_RATES_API_SOURCE

def parse_exchange_rate_response(json_response: dict) -> list:
    return [
        {
            "source": EXCHANGE_RATE_API_SOURCE,
            "rates": {k : (1 / v) for k,v in json_response['conversion_rates'].items()}
        }
    ]

def parse_float_rates_response(json_response: dict) -> list:
    return [
        {
            "source": FLOAT_RATES_API_SOURCE,
            "rates": {v['code'] : float(v['inverseRate']) for v in json_response.values()}
        }
    ]

def parse_coin_gecko_response(json_response: dict) -> list:
    return [
        {
            "source": COIN_GECKO_API_SOURCE,
            "rates": {
                'BTC' : json_response['bitcoin']['usd'],
                'ETH' : json_response['ethereum']['usd'],
                'SOL' : json_response['solana']['usd']
            }
        }
    ]