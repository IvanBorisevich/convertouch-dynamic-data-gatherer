import motor.motor_asyncio
from pymongo import DeleteOne, ReplaceOne
import datetime
import traceback
import sys

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.convertouch_dynamic_data

currency_rate_collection = database.get_collection("currency_rates")



def to_flat_map(currency_rate_doc) -> dict:
    result = {}
    result[currency_rate_doc["code"]] = currency_rate_doc["coefficient"]
    return result


async def retrieve_currency_rates():
    currency_rates = {}
    async for currency_rate in currency_rate_collection.find():
        currency_rates.update(to_flat_map(currency_rate))
    return currency_rates


async def retrieve_currency_rate(code: str) -> dict:
    currency_rate = await currency_rate_collection.find_one({"code": code})
    if currency_rate:
        return to_flat_map(currency_rate)
    return {}
    
    
async def upsert_currency_rates(currency_rates_data: dict) -> dict:
    requests = [
        ReplaceOne({'code': key}, {'code': key, 'coefficient': currency_rates_data[key], 'modified': datetime.datetime.now()}, upsert=True)
        if currency_rates_data[key]
        else DeleteOne({'code': key})
        for key in currency_rates_data
    ]
    try:
        await currency_rate_collection.bulk_write(requests)
    except Exception as e:
        print("Error during upsert: ", format_exception(e))



def format_exception(e):
    exception_list = traceback.format_stack()
    exception_list = exception_list[:-2]
    exception_list.extend(traceback.format_tb(sys.exc_info()[2]))
    exception_list.extend(traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]))

    exception_str = "Traceback (most recent call last):\n"
    exception_str += "".join(exception_list)
    # Removing the last \n
    exception_str = exception_str[:-1]

    return exception_str
