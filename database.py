import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

db = SQLAlchemy()

def get_database_url():
    return os.getenv("DATABASE_URL", "sqlite:///database.db")
