"""
Main FastAPI Application Entrypoint.

This module initializes the FastAPI application, mounts all routers,
and sets up the application lifespan events (like starting the scheduler).
"""
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.scheduler.runner import start_scheduler, scheduler
from app.api.routes import opportunities

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handle the startup and shutdown lifecycle of the FastAPI application.

    Starts the APScheduler in the background when the server starts,
    and cleanly shuts it down when the server stops.
    """
    # Startup
    start_scheduler()
    yield
    # Shutdown
    scheduler.shutdown()

app = FastAPI(
    title="IEEE Opportunity Intelligence API", 
    description="API for accessing scheduled scrapes of IEEE student opportunities.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(opportunities.router, prefix="/opportunities", tags=["opportunities"])

@app.get("/health", tags=["system"])
async def health_check():
    """
    Health check endpoint.
    Used by orchestrators (like Docker/Kubernetes) to verify the service is running.
    """
    return {"status": "ok"}
