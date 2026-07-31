from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo import DeleteOne, ReplaceOne
import datetime
from env_manager import get_env_variable

connection_string = get_env_variable('ATLAS_URI')
db_name = get_env_variable('DB_NAME')

client = MongoClient(connection_string, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Successfully connected to MongoDB Atlas!")
except Exception as e:
    print("Error when trying to connect to the Atlas cluster: ", e)
else:
    database = client.get_database(db_name)
    currency_rate_collection = database.get_collection("currency_rates")


async def retrieve_currency_rates_sources() -> list:
    return [
        {
            'value': item['source']
        } 
        for item in currency_rate_collection.find({}, {"source": 1, "_id": 0})
    ]


async def retrieve_currency_rates(source: str):
    parsed_rates_map = currency_rate_collection.find_one({"source": source})
    return parsed_rates_map["rates"]


async def retrieve_currency_rate(source: str, code: str) -> dict:
    parsed_rates_map = await retrieve_currency_rates(source)
    
    result = {}
    result[code] = parsed_rates_map[code]
    return result
    
    
def upsert_currency_rates(currency_rates_data: list) -> list:
    requests = [
        ReplaceOne(
            {
                'source': parsed_rates_map['source']
            }, 
            {
                'source': parsed_rates_map['source'], 
                'rates': parsed_rates_map['rates'], 
                'modified': datetime.datetime.now()
            }, upsert=True
        ) for parsed_rates_map in currency_rates_data
    ]

    currency_rate_collection.bulk_write(requests)