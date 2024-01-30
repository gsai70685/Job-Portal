from fastapi import APIRouter, HTTPException, status, Depends, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError
from pymongo.database import Database
from datetime import timedelta, timezone, datetime
from schemas import (RegisterUser, settings, TokenModel, UserModel,
                     HRInformation, AdminInformation)
from utils import hash_password, verify_password
from database import get_mongo_db
import oauth2
from middlewares.auth_middleware import get_current_user
from typing import Annotated
from email.utils import format_datetime
import json

router = APIRouter()

ACCESS_TOKEN_EXPIRES_IN = settings.SECRET

@router.post("/register",status_code=status.HTTP_201_CREATED,
             summary="This route will take care of registeration for all type of users")
async def register_user(payload:RegisterUser, db: Database = Depends(get_mongo_db)):
    """
    Here on the basis of the user role we are going to register his/her
    account, and if something goes wrong we are going to throw the error
    """
    store_data = True

    if payload.role == "HR":
        # Validate and process the HR information
        if payload.hr_info:
            try:
                HRInformation.model_validate(payload.hr_info)
            except ValidationError as e:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Invalid HR Information: {e}"
                )
            else:
                # Reassigning it, just to insure the type consistency
                payload.hr_info = payload.hr_info
        else:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="HR Information missing..."
            )

    elif payload.role == "Admin":
        # Validating the Admin info
        if payload.admin_info:
            try:
                AdminInformation.model_validate(payload.admin_info)
            except ValidationError as e:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Invalid Admin Information: {e}"
                )
            else:
                if payload.admin_info.admin_key != settings.ADMIN_KEY:
                    raise HTTPException(
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"Invalid Admin Key"
                    )
                # Reassigning it, just to insure the type consistency
                payload.admin_info = payload.admin_info
        else:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Admin Information missing..."
            )

    elif payload.role == "User":
        store_data = True

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user role provided.",
        )

    if store_data:
        with get_mongo_db() as db:
            print("Inside")
            users_collection = db["users"]
            existing_user_email = users_collection.find_one({"email":payload.email.lower()})
            if existing_user_email:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Email already taken")
            existing_username = users_collection.find_one({"username":payload.username})
            if existing_username:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Username already taken")
            payload.password = await hash_password(payload.password)
            payload.email = payload.email.lower()
            data_ = payload.model_dump()
            users_collection.insert_one(data_)
            return {"message":f"Account created for {payload.username}"}

@router.post("/login", status_code=status.HTTP_200_OK, response_model=TokenModel)
async def user_login(payload: OAuth2PasswordRequestForm = Depends(),
               db:Database = Depends(get_mongo_db)):
    with get_mongo_db() as db:
        users = db["users"]
        user_exists = users.find_one({"username":payload.username})
        if user_exists:
            hashed_password = user_exists["password"]
            if await verify_password(payload.password, hash_password=hashed_password):
                # We will generate token here
                userdata = {"sub":user_exists["email"], "role":user_exists["role"]}
                access_token, exp = await oauth2.create_access_token(userdata)
                response_data = {"role": str(user_exists["role"])}
                user_found_json = json.dumps(response_data)
                response = Response(content=user_found_json)
                exp_utc = exp.replace(tzinfo=timezone.utc)
                formatted_expiry = format_datetime(exp_utc, usegmt=True)
                response.set_cookie(key="access_token", value=access_token, domain="127.0.0.1", httponly=True, secure=True, samesite="none", expires=formatted_expiry)
                # return {"access_token":access_token, "token_type":"bearer"}
                return response
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                 detail="Wrong credentials!!")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="Wrong credentials")

@router.get("/logout")
async def logout_user(response:Response , current_user: Annotated[UserModel, Depends(get_current_user)]):
    # Here we will write the logic to delete the access token from the user cookies
    # for now we are just deleting the token from the browser of the user later will find the another way to handle the same
    if current_user:
        # current_datetime = datetime.now()
        # expiration_duration = timedelta(days=2)
        # past_expiration_datetime = current_datetime - expiration_duration
        # past_expiration_str = past_expiration_datetime.strftime("%a, %d %b %Y %H:%M:%S GMT")
        response.set_cookie(key="access_token", value="", expires=0, max_age=0, httponly=True, samesite="None", path="/", secure=True)

        return {"message":"User Logged out!!"}

@router.post("/account", status_code=status.HTTP_200_OK)
async def get_account_data(current_user: Annotated[UserModel, Depends(get_current_user)]):
    if current_user:
        return current_user
