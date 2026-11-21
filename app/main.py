
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.leads import router as leads_router

from app.database.connection import (
    connect_database,
    close_database
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_database()

    yield
 
    await close_database()


app = FastAPI(
    title="CRM API",
    description="AI-powered lead management platform",
    version="1.0.0",
    lifespan=lifespan
)


app.include_router(leads_router)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected"
    }

