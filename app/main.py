from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings
from app.config.database import Database
from app.core.logging import setup_logging
from app.core.exceptions import CustomHTTPException, http_exception_handler, validation_exception_handler
from app.api.v1.routes import api_router
from loguru import logger
from pydantic import ValidationError
import os
from mangum import Mangum

from dotenv import load_dotenv

def create_application() -> FastAPI:
    load_dotenv()

    setup_logging()

    # logger.info(f"ACCESS_KEY_ID_AWS: {os.getenv('ACCESS_KEY_ID_AWS')}")
    # logger.info(f"SECRET_ACCESS_KEY_AWS: {os.getenv('SECRET_ACCESS_KEY_AWS')}")
    # logger.info(f"REGION_AWS: {os.getenv('REGION_AWS')}")

    application = FastAPI(
        title=settings.PROJECT_NAME,
        # openapi_url=f"{settings.API_V1_STR}/openapi.json",
    )

    #Initialize DB
    db = Database()
    db.initialize_db(application)

    # Set CORS middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin)
                       for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add exception handlers
    application.add_exception_handler(
        CustomHTTPException, http_exception_handler)
    application.add_exception_handler(
        ValidationError, validation_exception_handler)

    # Include API routes
    application.include_router(api_router, prefix=settings.API_V1_STR)

    return application


app = create_application()

@app.get("/")
def read_root():
    return {"message": "CWLE API is running"}


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up FastAPI application")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down FastAPI application")

# mangum to read application instance for aws readability
handler = Mangum(app)
