import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Fetch secret values from environment
SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY')

DEFAULT_IMAGE_URL = "https://ibb.co/81mTf6g"