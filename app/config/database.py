from tortoise.contrib.fastapi import register_tortoise
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from loguru import logger

from app.config.settings import settings

# # Load environment variables
# load_dotenv()

class Database:
    def __init__(self):
        # self.db_uri = os.getenv('DB_URI')
        self.db_uri = settings.DATABASE_URL
        if not self.db_uri:
            raise ValueError("DB_URI environment variable is not set")

    def initialize_db(self, app: FastAPI):
        """Initializes the database with FastAPI"""
        logger.info("Initializing database...")
        
        register_tortoise(
            app,
            db_url=self.db_uri,
            modules={
                'models': [
                    'app.models.chat_history',  # Add the chat history model here
                ]
            },
            generate_schemas=True,
            add_exception_handlers=True
        )
        
        logger.info("Database initialized successfully.")
