# app/config.py
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./mamatoto.db"
    
    # Security
    secret_key: str = "your-super-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24 hours
    
    # API
    api_title: str = "Mamatoto API"
    api_version: str = "1.0.0"
    api_description: str = "Maternal and Child Health Platform API"
    
    # CORS
    allowed_origins: list = ["http://localhost:3000","https://3000-firebase-mamatotogit-1753969026312.cluster-64pjnskmlbaxowh5lzq6i7v4ra.cloudworkstations.dev", "http://localhost:5173"]
    
    # OpenAI (for chatbot)
    openai_api_key: str = ""
    
    # SMS/Notifications (future)
    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    
    class Config:
        env_file = ".env"

settings = Settings()