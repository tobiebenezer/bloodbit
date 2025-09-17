import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base config, uses local .env file."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'a-fallback-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///instance/db.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('SECRET_KEY', 'a-fallback-jwt-secret-key')
