from fastapi import Depends,Request
from jose import jwt
from schemas import settings
from database import get_mongo_db
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from pymongo.database import Database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_token_from_cookies(request: Request):

    return request.cookies.get("access_token")

async def create_access_token(data: dict, expires_delta: timedelta | None=None,
                              db:Database=Depends(get_mongo_db)):
    to_encode = data.copy()
    if expires_delta:
        expires = datetime.utcnow() + expires_delta
    else:
        expires = datetime.utcnow() + timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRES_IN))
    to_encode.update({"exp":expires})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET, algorithm=settings.JWT_ALGORITHM)
    return (encoded_jwt, expires)


