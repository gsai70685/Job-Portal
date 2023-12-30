from fastapi import APIRouter, HTTPException, Depends, status
from typing import Annotated
import oauth2
from schemas import UserModel
from models import JobModel
from pymongo.database import Database
from database import get_jobs_mongo_db
from bson import json_util
import json

router = APIRouter()

@router.get("/all", status_code=status.HTTP_200_OK,
            summary="This gives only 100 jobs in starting")
def get_all_jobs(
                current_user:Annotated[UserModel, Depends(oauth2.get_current_user)],
                 db:Database = Depends(get_jobs_mongo_db)
                ):
    if current_user:
        with get_jobs_mongo_db() as db:
            jobs_collection = db["jobs_meta"]
            all_jobs = jobs_collection.find().limit(20)
            all_jobs_list = list(all_jobs)
            json_result = json.dumps(all_jobs_list, default=json_util.default())
            return json_result
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Credentials Not Verified!!",
                            headers={"WWW-Authenticate":"Bearer"})


@router.post("/post", status_code=status.HTTP_201_CREATED,
             summary="This helps in adding job to our web app")
def add_job(
            payload:JobModel,
            current_user:Annotated[UserModel, Depends(oauth2.get_current_user)],
            db:Database = Depends(get_jobs_mongo_db)
            ):
    if current_user and (current_user["role"] == "Admin" or current_user["role"] == "HR"):
        with get_jobs_mongo_db() as db:
            jobs_collection = db["jobs_meta"]
            jobs_collection.insert_one(payload)
            return {"message":"Job Added"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized for this action"
    )

