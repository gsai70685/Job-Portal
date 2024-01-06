from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime
from typing import List, Optional


class JobModel(BaseModel):
    company : str
    job_title : str
    skills : str | None=None
    experience : str | None=None
    job_id : str | None=None
    job_type : str | None=None
    location : str | None=None
    date_posted : str | None=None
    job_description : str | None=None
    twitter : str = Field(...)
    websites : str = Field(...)
    qualification : str | None=None
    job_url : str = Field(...)
    added : str = Field(...)
    updated : str = Field(...)


class JobModel_for_home_page(BaseModel):
    
    id: str
    company: str
    job_title: str
    job_type: str
    location: str
    date_posted: str
    job_description: str
    job_url: str
    job_id: str
    websites: str
    twitter: str
    experience: str
    added: datetime
    updated: datetime
    qualification: Optional[str] = ""
    skills: Optional[str] = ""