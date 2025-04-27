from fastapi import APIRouter
from app.api.endpoints.auth import router as auth_router
from app.api.endpoints.user import router as user_router

router = APIRouter()

# Include all routers
router.include_router(auth_router, prefix="/auth/user", tags=["auth"])
router.include_router(user_router, prefix="/user", tags=["user"])
