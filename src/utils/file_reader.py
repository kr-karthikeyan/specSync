import os
from dotenv import load_dotenv

# Load all variables from .env file into memory
load_dotenv()

def get_api_key(provider: str = "groq") -> str:
    """
    Reads the API key for the chosen provider from environment variables.
    
    provider: "openai" or "groq"
    returns: the API key as a string
    """
    # Choose which env variable to look for based on provider
    if provider == "groq":
        env_var = "GROQ_API_KEY"
    else:
        env_var = "OPENAI_API_KEY"
    
    # Fetch the key from environment
    key = os.getenv(env_var)
    
    # If key is missing, give a clear helpful error
    if not key:
        raise ValueError(f"{env_var} not found. Check your .env file.")
    
    return key