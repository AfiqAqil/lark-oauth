from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Lark OAuth Integration"
    API_V1_STR: str = "/api/v1"
    
    # Lark OAuth settings
    LARK_APP_ID: str
    LARK_APP_SECRET: str
    LARK_BASE_URL: str = "https://open.larksuite.com"
    REDIRECT_URI: str
    
    # Database settings (if needed)
    DATABASE_URL: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings() 