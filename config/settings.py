import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")


    @classmethod
    def validate_keys(cls):
        missing_keys = []
        if not cls.GOOGLE_API_KEY:
            missing_keys.append("GOOGLE_API_KEY")
        if not cls.OPENWEATHERMAP_API_KEY:
            missing_keys.append("OPENWEATHERMAP_API_KEY")
        return missing_keys
