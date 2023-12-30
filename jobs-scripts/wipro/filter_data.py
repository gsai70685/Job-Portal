"""Code to update or insert data in the mongo db database"""
import pymongo
from dotenv import load_dotenv
import os
import datetime

load_dotenv()

# Retrieve MongoDB connection information from environment variables
username = os.environ.get("SERVER_USER")
password = os.environ.get("SERVER_PASS")
host = os.environ.get("HOST")
uri = f"mongodb://{username}:{password}@{host}:27017"

def main(data:dict, company=None):
    with pymongo.MongoClient(uri) as client:

        if company:
            result = check_data(company, data, client)
        else:
            result = add_data_to_statustable(data, client)
        return result

def add_data_to_statustable(data:dict, client)-> bool:
    database = client["JobStatus"]
    collection = database["scrapstatus"]
    existing_url = collection.find_one({"job_url": data["job_url"]})
    if existing_url:
        updated_data = {"scraped":data["scraped"]}
        collection.update_one({"_id":existing_url["_id"]}, {"$set":updated_data})
    else:
        collection.insert_one(data)
    return True

def check_data(company, data, client) ->bool:
    """
    Check and update job data in MongoDB collection.

    Args:
        company (str): The company name.
        data (dict): The job data to be checked and updated.

    Returns:
        None
    """
    client = pymongo.MongoClient(uri)
    database = client["jobsportal"]
    collection = database["jobs_meta"]

    existing_job = collection.find_one({"company": company, "job_url": data["job_url"]})
    if existing_job:
        new_data = [key for key in data.keys() if key not in ["updated" , "added"]]
        updated_data = {}
        for key in new_data:
            if data[key] != existing_job[key]:
                updated_data[key] = data[key]
        if updated_data:
            updated_data["updated"] = datetime.datetime.now()
            collection.update_one({"_id":existing_job["_id"]}, {"$set":updated_data})
            print(f"Job for {company} with job URL {data['job_url']} updated.")
        else:
            print(f"Job for {company} with job URL {data['job_url']} already up-to-date.")
    else:
        collection.insert_one(data)
        print(f"New job for {company} added with job URL {data['job_url']}.")
    return True


