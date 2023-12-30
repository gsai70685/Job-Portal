from pydantic import BaseModel, Field

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