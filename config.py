import os
from pathlib import Path
from dotenv import load_dotenv

# Base Directory
BASE_DIR = Path(__file__).resolve().parent

# Load .env file
load_dotenv(BASE_DIR / ".env")

# Database Credentials
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "securedoc_db")
DB_PORT = int(os.getenv("DB_PORT", 3306))

# Secret Key
SECRET_KEY = os.getenv("SECRET_KEY", "securedoc_ai_secret_2026")

# Temp storage folder
TEMP_DIR = BASE_DIR / os.getenv("TEMP_DIR", "temp_files")
TEMP_DIR.mkdir(exist_ok=True, parents=True)

# Risk Threshold Weights
RISK_WEIGHTS = {
    "Aadhaar": 10,
    "PAN": 10,
    "Password": 15,
    "API Key": 15,
    "Credit Card": 12,
    "Phone Number": 5,
    "Email": 3,
}

RISK_LEVELS = {
    "HIGH": 20,    # Score >= 20
    "MEDIUM": 8,   # Score >= 8
    "LOW": 0       # Score < 8
}
