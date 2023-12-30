from pydantic import BaseModel, constr, EmailStr, Field, validator, ValidationError
from pydantic_settings import BaseSettings
from typing import Optional
from datetime import datetime

class RegisterUser(BaseModel):
    username: constr(max_length=10)
    password: constr(min_length=8, max_length=32)
    email: EmailStr = Field(...)
    role: str = "User"

    @validator("password")
    @classmethod
    def validate_password(cls, value):
        errors = []

        # Ensure at least one uppercase letter
        if not any(char.isupper() for char in value):
            errors.append("Password must contain at least one uppercase letter")

        # Ensure at least one digit
        if not any(char.isdigit() for char in value):
            errors.append("Password must contain at least one digit")

        # Ensure at least one symbol
        if not any(char.isascii() and not char.isalnum() for char in value):
            errors.append("Password must contain at least one symbol")

        if errors:
            raise ValueError(errors, cls)

        return value

class Settings(BaseSettings):
    SERVER_USER : str
    SERVER_PASS : str
    SERVER_HOST :str
    SERVER_DB : str
    ACCESS_TOKEN_EXPIRES_IN: str
    JWT_ALGORITHM : str
    SECRET : str
    ADMIN_KEY:str
    HR_KEY:str

    class Config:
        env_file = ".env"
settings = Settings()

class LoginSchema(BaseModel):
    email : EmailStr
    password: str

class AdminRegisterModel(RegisterUser):
    admin_key:str
    role:str = "Admin"

class HrRegisterModel(RegisterUser):
    hr_key:str
    role:str = "HR"

class UserModel(BaseModel):
    username : str
    email : EmailStr
    role : str

class TokenModel(BaseModel):
    access_token: str
    token_type : str

class TokenData(BaseModel):
    email: EmailStr | None = None

class BlogCreate(BaseModel):
    title: str = ...
    description: str = ...
    image: Optional[str] |  None
    updated_at : Optional[datetime] = datetime.utcnow()
    created_at : Optional[datetime] = datetime.utcnow()