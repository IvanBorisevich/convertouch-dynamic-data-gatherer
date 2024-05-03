import motor.motor_asyncio
from bson.objectid import ObjectId

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.convertouch_dynamic_data

currency_rate_collection = database.get_collection("currency_rates")


# helpers


def currency_rate_helper(currency_rate) -> dict:
    return {
        "id": str(currency_rate["_id"]),
        "code": currency_rate["code"],
        "coefficient": currency_rate["coefficient"]
    }


async def retrieve_currency_rates():
    currency_rates = []
    async for currency_rate in currency_rate_collection.find():
        currency_rates.append(currency_rate_helper(currency_rate))
    return currency_rates


async def add_currency_rate(currency_rate_data: dict) -> dict:
    currency_rate = await currency_rate_collection.insert_one(currency_rate_data)
    new_currency_rate = await currency_rate_collection.find_one({"_id": currency_rate.inserted_id})
    return currency_rate_helper(new_currency_rate)


async def retrieve_currency_rate(id: str) -> dict:
    currency_rate = await currency_rate_collection.find_one({"_id": ObjectId(id)})
    if currency_rate:
        return currency_rate_helper(currency_rate)