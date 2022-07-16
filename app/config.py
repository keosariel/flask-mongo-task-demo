import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    DEBUG = True  # some Flask specific configs
    MONGO_URI = os.getenv("MONGO_URI")