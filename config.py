import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Flask settings
    SECRET_KEY = os.getenv("SECRET_KEY")
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"

    # Google Login
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")


config = Config()
