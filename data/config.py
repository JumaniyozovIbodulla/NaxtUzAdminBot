from dotenv import load_dotenv
from os import getenv
load_dotenv(override=True)

BOT_TOKEN = getenv("BOT_TOKEN")
ADMINS = getenv("ADMINS")
BASE_URL = getenv("BASE_URL")

# You can write another configs from .env file
