from fastapi import APIRouter, HTTPException, status, Depends, Response
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from pymongo.database import Database
from datetime import timedelta, timezone
from email.utils import format_datetime
from schemas import RegisterUser, settings, TokenModel
from utils import hash_password, verify_password
from database import get_mongo_db
import oauth2 
from typing import Annotated

router = APIRouter()

ACCESS_TOKEN_EXPIRES_IN = settings.SECRET

@router.post("/register",status_code=status.HTTP_201_CREATED)
async def register_user(payload:RegisterUser, db: Database = Depends(get_mongo_db)):
    with get_mongo_db() as db:
        users_collection = db["users"]
        existing_user_email = users_collection.find_one({"email":payload.email.lower()})
        if existing_user_email:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                 detail="Email already taken")
        existing_username = users_collection.find_one({"username":payload.username})
        if existing_username:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                 detail="Username already taken")
        print(payload, type(payload))
        hashed_password = await hash_password(payload.password)
        print(hashed_password)
        payload.password = hashed_password
        payload.email = payload.email.lower()
        payload.role = "User"
        data_ = payload.model_dump()
        #print(data_, type(data_))
        users_collection.insert_one(data_)
        return {"message":f"Account created for {payload.username}"}

@router.post("/login", status_code=status.HTTP_200_OK, response_model=TokenModel)
async def user_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
               db:Database = Depends(get_mongo_db)):
    with get_mongo_db() as db:
        collection = db["users"]
        user_exists = collection.find_one({"email":form_data.username})
        #print(user_exists)
        if user_exists:
            hashed_password = user_exists["password"]
            if await verify_password(form_data.password, hash_password=hashed_password):
                # We will generate token here
                userdata = {"sub":user_exists["email"], "role":user_exists["role"]}
                access_token, exp= await oauth2.create_access_token(userdata)
                #print(access_token, exp)
                response = JSONResponse(content= {"message":"Login successful"})
                #response = Response()
                exp_utc = exp.replace(tzinfo=timezone.utc)
                formatted_expiry = format_datetime(exp_utc, usegmt=True)
                print(formatted_expiry)

                
                
                response.set_cookie(key="access_token", 
                                    value=access_token,
                                    httponly=True,
                                    expires=formatted_expiry, 
                )       # SOS: Always change and add a domain parameter for front end 
                # print(response)
                # print(response.body)
                #print(response.cookies)
                
                return response
        
                #return {"access_token":access_token, "token_type":"bearer"}
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                 detail="Wrong credentials!!")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="Wrong credentials")
