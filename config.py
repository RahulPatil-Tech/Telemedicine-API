import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://rp32:Strong%40123@localhost:5432/telemedicine_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'a_strong_and_random_fallback_secret_key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'a_different_strong_and_random_jwt_key')