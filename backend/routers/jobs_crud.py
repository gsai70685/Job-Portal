from fastapi import APIRouter, HTTPException, Depends, status, Query
from typing import Annotated
import oauth2
from schemas import UserModel
from models import JobModel
from pymongo.database import Database
from database import get_jobs_mongo_db
from bson import json_util
import json
from bson.objectid import ObjectId


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
            all_jobs = jobs_collection.find()
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

@router.get("/jobs-home/", response_model=dict)
async def get_fifty_jobs(last_object_id: str = Query(None, description="Last Object ID from the previous request"), db=Depends(get_jobs_mongo_db)):
    with get_jobs_mongo_db() as db:
        collection = db["jobs_meta"]
        query = {"_id": {"$gt": ObjectId(last_object_id)}} if last_object_id else {}
        jobs = collection.find(query).limit(50)

        job_data = [
            {
                "id": str(job["_id"]),  # Convert ObjectId to string
                "company": job["company"],
                "title": job["job_title"],
                "type": job["job_type"],
                "location": job["location"],
                "date_posted": job["date_posted"],
                "job_description": job["job_description"],
                "job_url": job["job_url"],
                "job_id": job["job_id"],
                "websites": job["websites"],
                "twitter": job["twitter"],
                "experience": job["experience"],
                "added": job["added"],
                "updated": job["updated"],
                "qualification": job.get("qualification", ""),
                "skills": job.get("skills", ""),
            } for job in jobs
        ]

        last_object_id_in_page = str(job_data[-1]["id"]) if job_data else last_object_id

        return {"jobs": job_data, "last_object_id": last_object_id_in_page}

