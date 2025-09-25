"""FastAPI application entrypoint and configuration.

Description: Creates the FastAPI app, configures CORS, and registers routes.
"""

# Import asynccontextmanager for managing FastAPI lifespan events asynchronously
# Import asynccontextmanager to manage FastAPI lifespan events asynchronously
from contextlib import asynccontextmanager
# Import AsyncGenerator for type hinting asynchronous generator functions
from typing import AsyncGenerator

# Import FastAPI main class for creating the application instance
from fastapi import FastAPI
# Import CORS middleware to handle cross-origin requests
from fastapi.middleware.cors import CORSMiddleware
# Import database engine and base class for ORM table creation
from .db import engine, Base
# Import application settings (e.g., allowed origins, database URL)
from .config import settings

# Define the FastAPI lifespan event handler using async context manager
@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan handler.

    Creates all database tables on startup and yields control back to FastAPI.
    No teardown actions are required on shutdown for this demo.
    """
    # On application startup, ensure all database tables are created
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # Yield control back to FastAPI (no teardown actions needed here)
    yield

# Create the FastAPI application instance, registering the lifespan handler
app = FastAPI(lifespan=lifespan)

# Add CORS middleware to allow cross-origin requests from allowed origins
app.add_middleware(
    CORSMiddleware,
    # Parse allowed origins from settings, splitting by comma and stripping whitespace
    allow_origins=[o.strip() for o in settings.allowed_origins.split(",") if o.strip()],
    allow_credentials=True,  # Allow cookies and authentication headers
    allow_methods=["*"],     # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],     # Allow all headers
)

# Define a simple health check endpoint to verify the API is running
@app.get("/health")
async def health() -> dict:
    """Health check endpoint used for liveness/readiness probes."""
    return {"status": "ok"}

# Import the API router for item-related endpoints
from .routes import router as items_router

# Register the item router with the FastAPI application
app.include_router(items_router)


