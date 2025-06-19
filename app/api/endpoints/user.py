from fastapi import APIRouter, HTTPException, status

from app.core.models import users_db, auth_db
from app.core.logger import logger

router = APIRouter()


@router.get("/{user_id}")
async def get_user(user_id: str):
    """Get user information by user ID."""
    try:
        # Check if user exists
        if user_id not in users_db:
            logger.error(f"User not found: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
            
        # Get user and auth information
        user = users_db[user_id]
        auth = auth_db.get(user_id)
        
        if not auth:
            logger.error(f"Auth information not found for user: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Auth information not found"
            )
            
        # Return user data and token information
        return {
            "user": user.dict(),
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
        logger.error(f"Error getting user information: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user information"
        ) 