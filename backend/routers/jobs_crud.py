import os
from fastapi import APIRouter, HTTPException, Depends, status, Query, Request, Form
from fastapi.responses import JSONResponse
from typing import Annotated, List
from middlewares.auth_middleware import get_current_user
from schemas import UserModel, FilterJobRequestData
from models import JobModel
from pymongo.database import Database
from database import get_mongo_db
from bson import json_util, ObjectId
from utils import foldername
from middlewares.image_middleware import save_image
import json

router = APIRouter()

@router.post("/all", status_code=status.HTTP_200_OK,
            summary="This gives only 50 jobs in starting")
async def get_all_jobs(
                jobfilters:FilterJobRequestData,
                current_user:Annotated[UserModel, Depends(get_current_user)],
                last_item: str = Query(None, description="Id of the last job item"),
                limit: int = Query(10, description="Number of jobs per page"),
                direction: str = Query(None, description="Pagination direction: 'next' or 'previous'"),
                db:Database = Depends(get_mongo_db)
                ):
    if current_user:
        pipeline = []
        jobtype_conditions = []
        if jobfilters.keyword:
            keyword_regex = {"$regex": jobfilters.keyword.lower(), "$options": "i"}
            pipeline.append(
                {
                    "$match": {
                        "$or": [
                            {"job_title": keyword_regex},
                            {"company": keyword_regex}
                        ]
                    }
                }
            )
        if jobfilters.location:
            location_regex = {"$regex": jobfilters.location.lower(), "$options": "i"}
            pipeline.append({
                "$match": {"location": location_regex}
            })
        if jobfilters.filters:
            jobtype_conditions = []
            # Check if "others" is in the filters, if yes, exclude certain types
            if "others" in jobfilters.filters:
                excluded_types = ["full time", "freelance", "part time", "temporary", "internship", "fulltime", "Full Time"]
                jobtype_conditions.append({"job_type": {"$nin": excluded_types}})
            else:
                jobtype_conditions = [{"job_type": {"$regex": f"{filter}", "$options": "i"}} for filter in jobfilters.filters]
            # Append the match condition to the pipeline
            pipeline.append({"$match": {"$or": jobtype_conditions}})


        if last_item and direction == "next":
            pipeline.append({"$sort": {"_id": -1}})
            pipeline.append({"$match": {"_id": {"$lt": ObjectId(last_item)}}})

        elif last_item and direction == "prev":
            # pipeline.append({"$sort": {"_id": 1}})
            pipeline.append({"$match": {"_id": {"$gt": ObjectId(last_item)}}})


        else:
            pipeline.append({"$sort": {"_id": -1}})

        pipeline.append({
            "$project": {
                "job_title": 1,
                "location": 1,
                "date_posted": 1,
                "job_url": 1,
                "_id": 1,
                "job_type":1,
                "company":1
            }
        })
        pipeline.append({"$limit": limit})

        with get_mongo_db() as db:
            jobs_collection = db["jobs_meta"]
            all_jobs = jobs_collection.aggregate(pipeline)

                        ## Convert ObjectId to string for all items in the list
            all_jobs_list = [{"_id": str(job["_id"]),
                              "job_title": job["job_title"],
                              "location": job["location"],
                              "date_posted": job["date_posted"],
                              "job_url": job["job_url"],
                              "job_type":job["job_type"], "company":job["company"]} for job in all_jobs]
            # Get the last job ID if available
            if direction == "prev":
                all_jobs_list = all_jobs_list[::-1]

            last_job_id = str(all_jobs_list[-1]["_id"]) if all_jobs_list else None

            response_data = {"jobs": all_jobs_list, "last_job_id": last_job_id}
            return JSONResponse(content=response_data)

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Credentials Not Verified!!",
                            headers={"WWW-Authenticate":"Bearer"})

@router.get("/home", status_code=status.HTTP_200_OK)
def get_jobs_home(db:Database = Depends(get_mongo_db)):
    try:
        with get_mongo_db() as db:
            jobs_collection = db["jobs_meta"]
            projection = { "_id": 1, "job_title": 1, "location": 1, "date_posted": 1, "job_url":1, "job_type":1, "company":1}
            # Use projection in find to select specific columns
            all_jobs = jobs_collection.find({}, projection).sort("_id", -1).limit(3)

            all_jobs_list = [{"_id": str(job["_id"]),
                              "job_title": job["job_title"],
                              "location": job["location"],
                              "date_posted": job["date_posted"],
                              "job_url": job["job_url"],
                              "job_type":job["job_type"], "company":job["company"]} for job in all_jobs]
            return JSONResponse(content=all_jobs_list)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong"
        )


@router.post("/postjob", status_code=status.HTTP_201_CREATED,
             summary="Route to add jobs in databas eby Admin and HR only")
async def upload_job_data(
                    current_user:Annotated[UserModel, Depends(get_current_user)],
                    job_data:JobModel = Depends(JobModel.as_form),
                    db:Database = Depends(get_mongo_db)
                ):
    """
    Need to fix the changes here:
    What if the user doesnot provide any logo, handle that conditon
    """
    if current_user:
        logo_path = os.path.join(foldername, job_data.logo.filename)
        filedata =await job_data.logo.read()
        image_saved, error = await save_image(logo_path, filedata)
        if image_saved:
            with get_mongo_db() as db:
                collection = db["jobs_meta"]
                job_data.logo = logo_path
                collection.insert_one(job_data.model_dump())
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error
            )
        return {"message":"Job posted successfully"}

@router.get("/job", status_code=status.HTTP_200_OK)
def get_individula_job(
    request:Request,
    current_user: Annotated[UserModel, Depends(get_current_user)],
    jobid:str = Query(None, description="Id of the job, to get the data of it"),
    db:Database = Depends(get_mongo_db)
):
    if current_user:
        if jobid:
            with get_mongo_db() as db:
                job_collection = db["jobs_meta"]
                joblisting = job_collection.find_one({"_id":ObjectId(jobid)})
                if joblisting:
                    joblisting["_id"] = str(joblisting["_id"])
                    return json.loads(json_util.dumps(joblisting))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No job id given"
        )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You are unauthorized for this request"
    )

