from fastapi import Depends, HTTPException, status, Request
from jose import jwt, ExpiredSignatureError, JWTError
from schemas import settings, TokenData
from database import get_mongo_db
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from pydantic import EmailStr
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
    return encoded_jwt, expires

async def get_user(email:str, db:Database = Depends(get_mongo_db)):
    with get_mongo_db() as db:
        collection = db["users"]
        is_user = collection.find_one({"email":email})
        if is_user:
            return {"username":is_user["username"], "email":is_user["email"],
                    "role":is_user["role"]}


async def get_current_user(token:Annotated[str, Depends(oauth2_scheme)]):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"}
    )
    try:
        print(token)
        payload = jwt.decode(token, settings.SECRET, algorithms=[settings.JWT_ALGORITHM])
        email: EmailStr = payload.get("sub")
        if email is None:
            raise credential_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credential_exception
    user = await get_user(email=token_data.email)
    if user is None:
        raise credential_exception
    print(user)
    return user
