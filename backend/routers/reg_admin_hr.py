"""
This one will be a sepaarte route and for the frontend also it will not
be visible
"""

from fastapi import APIRouter, HTTPException, Depends, status
from database import get_mongo_db
from schemas import settings, AdminRegisterModel, HrRegisterModel
from pymongo.database import Database
from utils import hash_password

router = APIRouter()

@router.post("/admin", status_code=status.HTTP_200_OK,
             summary="To create admin account")
async def create_admin(payload:AdminRegisterModel,
                 db:Database=Depends(get_mongo_db)):
    with get_mongo_db() as db:
        collection = db["users"]
        existing_admin = collection.find_one({"username":payload.username})
        if existing_admin:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Account already there with the credentials!!")
        if payload.admin_key != settings.ADMIN_KEY:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Invalid credentials")
        payload.password = await hash_password(payload.password)
        payload.email = payload.email.lower()
        data_ = {"username":payload.username, "email":payload.email,
                 "password":payload.password, "role":payload.role}
        collection.insert_one(data_)
        return {"message":f"Account created for {payload.username}"}

@router.post("/hr", status_code=status.HTTP_200_OK,
             summary="To create Hr account")
async def create_admin(payload:HrRegisterModel,
                 db:Database=Depends(get_mongo_db)):
    with get_mongo_db() as db:
        collection = db["users"]
        existing_admin = collection.find_one({"username":payload.username})
        if existing_admin:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Account already there with the credentials!!")
        if payload.hr_key != settings.HR_KEY:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Invalid credentials")
        payload.password = await hash_password(payload.password)
        payload.email = payload.email.lower()
        data_ = {"username":payload.username, "email":payload.email,
                 "password":payload.password, "role":payload.role}
        collection.insert_one(data_)
        return {"message":f"Account created for {payload.username}"}