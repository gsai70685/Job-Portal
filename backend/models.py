from fastapi import Form, UploadFile
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class JobModel(BaseModel):
    company: Optional[str]
    job_title: Optional[str]
    date_posted : Optional[str] = None
    job_id: Optional[str] = None
    skills: Optional[str] = None
    description : Optional[str] = None
    experience: Optional[str] = None
    job_type: Optional[str] = None
    location: Optional[str] = None
    twitter: Optional[str] = None
    websites: Optional[str] = None
    qualifications: Optional[str] = None
    job_description : Optional[str] = None
    job_url: Optional[str]
    salary: Optional[str] = None
    logo: Optional[UploadFile] = None
    added : Optional[datetime] = datetime.today()
    updated: Optional[datetime] = datetime.today()

    @classmethod
    async def as_form(cls,
                      company: Optional[str] = Form(...),
                        job_title: Optional[str] = Form(...),
                        skills: Optional[str] = Form(None),
                        experience: Optional[str] = Form(None),
                        job_type: Optional[str] = Form(None),
                        location: Optional[str] = Form(None),
                        twitter: Optional[str] = Form(None),
                        websites: Optional[str] = Form(None),
                        qualifications: Optional[str] = Form(None),
                        job_description: Optional[str] = Form(None),
                        job_url: Optional[str] = Form(...),
                        salary: Optional[str] = Form(None),
                        logo: Optional[UploadFile] = Form(None)
                    ):
        return cls(job_title=job_title, company=company, skills=skills, experience=experience, job_type=job_type,
                   location=location, twitter=twitter, websites=websites, qualifications=qualifications, job_url=job_url,
                   salary=salary, logo=logo, job_description=job_description)

class BlogModel(BaseModel):
    title: str = Field(...)
    content: str  = Field(...)
    image: str | None=None
    created_at : Optional[datetime] = datetime.utcnow()
    updated_at: Optional[datetime] = datetime.utcnow()
    author: str = Field(...)

