from fastapi import APIRouter, HTTPException, status, Query
from fastapi.responses import RedirectResponse
import logging
import os

from app.core.config import settings
from app.services.lark_service import (
    get_user_access_token,
    get_user_info,
    create_or_update_user,
    refresh_access_token
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/lark/login")
async def lark_login():
    """Redirect to Lark authorization page."""
    auth_url = (
        f"{settings.LARK_BASE_URL}/authen/v1/authorize"
        f"?app_id={settings.LARK_APP_ID}"
        f"&redirect_uri={settings.REDIRECT_URI}"
        f"&response_type=code"
    )
    return RedirectResponse(url=auth_url)


@router.get("/lark/callback")
async def lark_callback(code: str = Query(...)):
    """Handle Lark callback with authorization code."""
    try:
        if not code:
            logger.error("Missing authorization code")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing authorization code"
            )
            
        # Exchange code for access token
        token_data = await get_user_access_token(code)
        if not token_data or "access_token" not in token_data:
            logger.error("Failed to get access token")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Failed to get access token"
            )
            
        # Get user info
        user_info = await get_user_info(token_data["access_token"])
        if not user_info:
            logger.error("Failed to get user info")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Failed to get user info"
            )
            
        # Create or update user and auth info
        result = await create_or_update_user(user_info, token_data)
        
        # Redirect to frontend with success
        # Check if we're using a separate frontend server
        frontend_url = os.environ.get("FRONTEND_URL", "http://localhost:3000")
        redirect_url = f"{frontend_url}/login-success.html?userId={result['user']['id']}"
        return RedirectResponse(url=redirect_url)
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error in Lark callback: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process Lark authentication"
        )


@router.post("/lark/refresh")
async def refresh_token(refresh_token: str):
    """Refresh the access token using a refresh token."""
    try:
        if not refresh_token:
            logger.error("Missing refresh token")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing refresh token"
            )
            
        # Refresh the token
        token_data = await refresh_access_token(refresh_token)
        if not token_data or "access_token" not in token_data:
            logger.error("Failed to refresh token")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Failed to refresh token"
            )
            
        return {
            "access_token": token_data["access_token"],
            "token_type": token_data.get("token_type", "Bearer"),
            "refresh_token": token_data["refresh_token"],
            "expires_at": token_data["expires_at"].isoformat(),
            "refresh_expires_at": token_data["refresh_expires_at"].isoformat()
        }
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error refreshing token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to refresh token"
        ) 