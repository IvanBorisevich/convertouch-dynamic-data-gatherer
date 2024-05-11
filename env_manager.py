from dotenv import dotenv_values
import os

config = dotenv_values(".env")

def get_env_variable(key: str):
    val = os.environ.get(key)

    if val == None:
        print('Variable "', key, '" not found on hosting, trying to get it from .env file')
        val = config[key]
    
    return val