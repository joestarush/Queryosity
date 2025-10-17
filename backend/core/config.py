import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    VECTOR_STORE_DIR = "backend/vector_store"
    UPLOAD_DIR = "backend/uploads"

settings = Settings()
