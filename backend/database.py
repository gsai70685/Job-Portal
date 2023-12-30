import pymongo
from schemas import settings
from contextlib import contextmanager
from urllib.parse import quote_plus

password_ = quote_plus(settings.SERVER_PASS)
uri = f"mongodb+srv://{settings.SERVER_USER}:{password_}@{settings.SERVER_HOST}/?retryWrites=true&w=majority"

@contextmanager
def get_mongo_db():
    client  = pymongo.MongoClient(uri)
    db = client["testingdb"]
    try:
        yield db
    finally:
        client.close()

@contextmanager
def get_jobs_mongo_db():
    client  = pymongo.MongoClient(uri)
    db = client["jobsportal"]
    try:
        yield db
    finally:
        client.close()

@contextmanager
def get_blogs_data_db():
    client = pymongo.MongoClient(uri)
    try:
        db = client["blogsdb"]
        yield db
    except Exception as e:
        print("Error occured while connecting to database. Errro: ", e)
    finally:
        client.close()