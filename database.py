import motor.motor_asyncio
from bson.objectid import ObjectId
from pymongo import InsertOne, DeleteOne, ReplaceOne

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
        ReplaceOne({'code': key}, {'code': key, 'coefficient': currency_rates_data[key]}, upsert=True)
        if currency_rates_data[key]
        else DeleteOne({'code': key})
        for key in currency_rates_data
    ]
    await currency_rate_collection.bulk_write(requests)
