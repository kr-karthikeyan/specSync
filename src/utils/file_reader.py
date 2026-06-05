import os
from dotenv from load_dotenv


load_dotenv()

def get_api_key:

    key = os.getenv("OPENAI_API_KEY")

    if not key:
        raise valueError("Key not found!")

    return key