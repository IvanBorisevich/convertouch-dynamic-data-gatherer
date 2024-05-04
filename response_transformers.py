def tranform_exchange_rate_api_response(json_response: dict) -> dict:
    return {k:(1 / v) for k,v in json_response['conversion_rates'].items()} 