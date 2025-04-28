import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Fetch secret values from environment
SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY')

DEFAULT_IMAGE_URL = "https://i.ibb.co/7sS8Z2t/Being.png"