from src.utils.file_reader import get_api_key
from src.generators.blueprint_generator import generate_blueprint

# Fetch from .env
api_key = get_api_key()

# Pass it down
blueprint = generate_blueprint(prd_text, api_key)