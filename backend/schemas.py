from pydantic import BaseModel, constr, EmailStr, Field, validator, ValidationError
from pydantic_settings import BaseSettings
from typing import Optional
from datetime import datetime
from bson import ObjectId


class AdminInformation(BaseModel):
    """
    This is the additional fields that are required for the
    admin login apart from HR and User
    """
    admin_key:str
    company : str = "Rivan Solutions"
    role:str = "Admin"

class HRInformation(BaseModel):
    """
    This is for adding additional info for the HR login
    """
    department : str
    company: str
    company_location: str
    role:str = "HR"

class RegisterUser(BaseModel):
    """
    This is the base model that is having the common details for the
    all type of users login
    """
    username: constr(max_length=10)
    password: constr(min_length=8, max_length=32)
    email: EmailStr = Field(...)
    created_at: datetime = datetime.now()
    role: str
    hr_info : HRInformation | None=None
    admin_info : AdminInformation | None = None

    @validator("password")
    @classmethod
    def validate_password(cls, value):
        """
        Here we are checking some parameters in our pasword,
        just for the saftey standards
        """
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
            raise ValueError(errors)

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

class UserModel(BaseModel):
    username : str
    email : EmailStr
    role : str

class TokenModel(BaseModel):
    access_token: str
    token_type : str

class TokenData(BaseModel):
    email: EmailStr | None = None

class BlogResponse(BaseModel):
    _id : ObjectId
    title: str = ...
    content: str = ...
    image: Optional[str] |  None
    updated_at : Optional[datetime] = datetime.utcnow()
    created_at : Optional[datetime] = datetime.utcnow()
    author: str = ...

class FilterJobRequestData(BaseModel):
    """
    This is for the request data for the job page,
    lastpageid will be passed as a query parameter and the
    rest in the json data format
    """
    keyword: str = ""
    location : str = ""
    filters : list[str] = []


