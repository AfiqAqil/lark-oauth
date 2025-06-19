from datetime import datetime, timedelta
from typing import Dict, Any
import httpx
from fastapi import HTTPException, status

from app.core.config import settings
from app.core.models import User, UserAuth, users_db, auth_db
from app.core.logger import logger


async def get_app_access_token() -> str:
    """Get an app access token from Lark."""
    try:
        url = f"{settings.LARK_API_BASE_URL}/auth/v3/app_access_token/internal"
        payload = {
            "app_id": settings.LARK_APP_ID,
            "app_secret": settings.LARK_APP_SECRET
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") != 0:
                logger.error(f"Failed to get app access token: {data.get('msg')}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"Failed to get app access token: {data.get('msg')}"
                )
                
            return data.get("app_access_token")
    except httpx.HTTPError as e:
        logger.error(f"HTTP error occurred: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Failed to communicate with Lark API"
        )
    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


async def get_user_access_token(code: str) -> Dict[str, Any]:
    """Exchange authorization code for user access token."""
    try:
        app_access_token = await get_app_access_token()
        url = f"{settings.LARK_API_BASE_URL}/authen/v1/oidc/access_token"
        headers = {"Authorization": f"Bearer {app_access_token}"}
        payload = {
            "grant_type": "authorization_code",
            "code": code
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") != 0:
                logger.error(f"Failed to get user access token: {data.get('msg')}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"Failed to get user access token: {data.get('msg')}"
                )
            
            token_data = data.get("data", {})
            # Calculate expiration times
            now = datetime.now()
            expires_in = token_data.get("expires_in", 7200)
            refresh_expires_in = token_data.get("refresh_expires_in", 2592000)
            
            token_data["expires_at"] = now + timedelta(seconds=expires_in)
            token_data["refresh_expires_at"] = now + timedelta(seconds=refresh_expires_in)
            
            return token_data
    except httpx.HTTPError as e:
        logger.error(f"HTTP error occurred: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Failed to communicate with Lark API"
        )
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


async def get_user_info(access_token: str) -> Dict[str, Any]:
    """Get user information using the access token."""
    try:
        url = f"{settings.LARK_API_BASE_URL}/authen/v1/user_info"
        headers = {"Authorization": f"Bearer {access_token}"}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") != 0:
                logger.error(f"Failed to get user info: {data.get('msg')}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"Failed to get user info: {data.get('msg')}"
                )
            
            return data.get("data", {})
    except httpx.HTTPError as e:
        logger.error(f"HTTP error occurred: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Failed to communicate with Lark API"
        )
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


async def refresh_access_token(refresh_token: str) -> Dict[str, Any]:
    """Refresh the access token using a refresh token."""
    try:
        app_access_token = await get_app_access_token()
        url = f"{settings.LARK_API_BASE_URL}/authen/v1/oidc/refresh_access_token"
        headers = {"Authorization": f"Bearer {app_access_token}"}
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") != 0:
                logger.error(f"Failed to refresh token: {data.get('msg')}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"Failed to refresh token: {data.get('msg')}"
                )
            
            token_data = data.get("data", {})
            # Calculate expiration times
            now = datetime.now()
            expires_in = token_data.get("expires_in", 7200)
            refresh_expires_in = token_data.get("refresh_expires_in", 2592000)
            
            token_data["expires_at"] = now + timedelta(seconds=expires_in)
            token_data["refresh_expires_at"] = now + timedelta(seconds=refresh_expires_in)
            
            return token_data
    except httpx.HTTPError as e:
        logger.error(f"HTTP error occurred: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Failed to communicate with Lark API"
        )
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


async def create_or_update_user(user_info: Dict[str, Any], token_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create or update a user and their authentication information."""
    try:
        # Extract required fields from user_info
        required_fields = ["open_id", "union_id", "name"]
        for field in required_fields:
            if field not in user_info:
                logger.error(f"Missing required field: {field}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Missing required user information: {field}"
                )
        
        # Check if user exists by open_id
        existing_user = None
        for user in users_db.values():
            if user.open_id == user_info["open_id"]:
                existing_user = user
                break
        
        if existing_user:
            # Update existing user
            user_id = existing_user.id
            user_data = {
                **existing_user.dict(),
                "name": user_info["name"],
                "email": user_info.get("email"),
                "avatar_url": user_info.get("avatar_url"),
                "updated_at": datetime.now()
            }
            users_db[user_id] = User(**user_data)
        else:
            # Create new user
            user = User(
                name=user_info["name"],
                email=user_info.get("email"),
                open_id=user_info["open_id"],
                union_id=user_info["union_id"],
                avatar_url=user_info.get("avatar_url")
            )
            user_id = user.id
            users_db[user_id] = user
        
        # Create or update user auth
        auth = UserAuth(
            user_id=user_id,
            access_token=token_data["access_token"],
            token_type=token_data.get("token_type", "Bearer"),
            refresh_token=token_data["refresh_token"],
            expires_at=token_data["expires_at"],
            refresh_expires_at=token_data["refresh_expires_at"]
        )
        auth_db[user_id] = auth
        
        # Return user data and token information
        return {
            "user": users_db[user_id].dict(),
            "auth": {
                "access_token": auth.access_token,
                "token_type": auth.token_type,
                "refresh_token": auth.refresh_token,
                "expires_at": auth.expires_at.isoformat(),
                "refresh_expires_at": auth.refresh_expires_at.isoformat()
            }
        }
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error creating/updating user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process user information"
        ) 