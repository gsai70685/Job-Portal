from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from database import get_mongo_db, get_blogs_data_db
from oauth2 import get_current_user
from pymongo.database import Database
from schemas import UserModel, BlogCreate
from bson.objectid import ObjectId

router = APIRouter()
@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_blog(
                        blog_data: BlogCreate,
                        current_user: Annotated[UserModel,Depends(get_current_user)],
                        db: Database = Depends(get_mongo_db)):
        print(current_user)
        if current_user and current_user["role"] != "Admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Only admins can create blogs.")
        author = current_user["username"]

        blog = {
        "title": blog_data.title,
        "description": blog_data.description,
        "image": blog_data.image,
        "created_date": blog_data.created_at,
        "updated_date": blog_data.updated_at,
        "author": author
        }
        with get_blogs_data_db() as db:
            collection = db["blogs"]
            data_inserted_instance = collection.insert_one(blog)
        if data_inserted_instance.inserted_id:
            return {"message": "Blog created successfully"}
        
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Failed to create blog")


@router.get("/blogs")
async def get_all_blogs(db = Depends(get_mongo_db)):
     with get_blogs_data_db() as db:
        collection = db["blogs"]
        blogs = collection.find()
        #print(blogs)
        blog_models = [BlogCreate(**blog) for blog in blogs]
        return blog_models

@router.get("/blogs/{blog_id}", response_model=BlogCreate)
async def get_blog_by_id(blog_id:str, db= Depends(get_mongo_db)):
     with get_blogs_data_db() as db:
        collection = db["blogs"]
        blog = collection.find_one({"_id": ObjectId(blog_id)})
        if blog:
            return blog
        else:
            raise HTTPException(status_code=404, detail="Blog not found")