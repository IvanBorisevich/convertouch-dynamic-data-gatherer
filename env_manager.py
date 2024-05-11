from dotenv import dotenv_values
import os

config = dotenv_values(".env")

def get_env_variable(key: str):
    val = os.environ.get(key)

    if val == None:
        val = config[key]
    
    return val