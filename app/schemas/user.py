from pydantic import BaseModel, EmailStr

class EmailSignupRequest(BaseModel):
    email: EmailStr

class EmailVerificationRequest(BaseModel):
    email: EmailStr
    code: str
    password: str

class OAuthSignupRequest(BaseModel):
    token: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
