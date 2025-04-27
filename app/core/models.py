from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
import uuid


class UserAuth(BaseModel):
    """Authentication information for a user."""
    user_id: str
    access_token: str
    token_type: str = "Bearer"
    refresh_token: str
    expires_at: datetime
    refresh_expires_at: datetime
    
    class Config:
        populate_by_name = True


class User(BaseModel):
    """User model for storing user information."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: Optional[str] = None
    open_id: str
    union_id: str
    avatar_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        populate_by_name = True


# In-memory storage for development/testing
users_db: dict[str, User] = {}
auth_db: dict[str, UserAuth] = {} 