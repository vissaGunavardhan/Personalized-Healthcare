import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'healthvault-abdm-personalized-portal-key-2026-vissa')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    DATABASE_PATH = BASE_DIR / 'data' / 'healthvault.db'
    UPLOAD_FOLDER = BASE_DIR / 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
    PORT = int(os.getenv('PORT', 5055))

    # Gemini model fallback hierarchy
    GEMINI_MODELS = [
        'gemini-3.5-flash',
        'gemini-3.8-flash',
        'gemini-flash-latest'
    ]
