from dotenv import load_dotenv
import os
# Creating separate .env file test and main
if os.environ.get("env") == "development":
    load_dotenv(".env_test")
else:
    load_dotenv(".env")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = "localhost"

CASTING_ASSISTANT_TOKEN = os.environ.get("CASTING_ASSISTANT_TOKEN")
CASTING_DIRECTOR_TOKEN = os.environ.get("CASTING_DIRECTOR_TOKEN")
EXECUTIVE_PRODUCER_TOKEN = os.environ.get("EXECUTIVE_PRODUCER_TOKEN")

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
API_AUDIENCE = os.environ.get("API_AUDIENCE")
ALGORITHMS = os.environ.get("ALGORITHMS")
