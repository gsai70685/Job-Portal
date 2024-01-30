import pymongo
from schemas import settings
from contextlib import contextmanager
from urllib.parse import quote_plus

password_ = quote_plus(settings.SERVER_PASS)
user = settings.SERVER_USER
userDB = settings.SERVER_DB

uri = f"mongodb+srv://{user}:{password_}@cluster0.y47qix4.mongodb.net/{userDB}"

@contextmanager
def get_mongo_db():
    client  = pymongo.MongoClient(uri)
    db = client[userDB]
    try:
        yield db
    finally:
        client.close()