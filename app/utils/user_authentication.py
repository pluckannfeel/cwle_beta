import random
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from tortoise.expressions import Q
from app.models.user import User
from app.config.settings import settings

SECRET_KEY = settings.SECRET_KEY
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
verification_codes = {}

class UserAuthentication:
    pass