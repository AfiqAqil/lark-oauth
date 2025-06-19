from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Lark OAuth Integration"

    # Lark OAuth settings
    LARK_APP_ID: str
    LARK_APP_SECRET: str
    LARK_API_BASE_URL: str = "https://open.larksuite.com/open-apis"
    LARK_AUTH_BASE_URL: str = "https://accounts.larksuite.com/open-apis"
    REDIRECT_URI: str
    
    # Database settings (if needed)
    DATABASE_URL: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings() 