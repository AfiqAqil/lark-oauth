from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager

from app.api.router import router
from app.core.config import settings
from app.core.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    # Startup logic
    logger.info("Starting Lark OAuth Integration API")
    yield
    # Shutdown logic
    logger.info("Shutting down Lark OAuth Integration API")


def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="A simple API for Lark OAuth authentication",
        version="0.1.0",
        lifespan=lifespan,
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(router, prefix="/api")

    # Mount static files (if needed)
    try:
        app.mount("/static", StaticFiles(directory="static"), name="static")
    except RuntimeError:
        # Handle case when static directory doesn't exist
        logger.warning("Static directory not found, skipping static file mounting")

    # Add root route to redirect to the guide
    @app.get("/")
    async def root():
        """Redirect to the setup guide."""
        return RedirectResponse(url="/static/index.html")

    return app


app = create_application()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="localhost", port=8000, reload=True)
