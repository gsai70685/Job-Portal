from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import Annotated, List
from database import get_mongo_db
from middlewares.auth_middleware import get_current_user
from pymongo.database import Database
from schemas import UserModel, BlogResponse
from models import BlogModel

router = APIRouter()

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_blog(
                            blog_data: BlogModel,
                            current_user: Annotated[UserModel,Depends(get_current_user)],
                            db: Database = Depends(get_mongo_db)):

    if current_user and current_user.role != "Admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Only admins can create blogs.")
    author = current_user.username
    # Save blog to the database
    blog = {
        "title": blog_data.title,
        "content": blog_data.content,
        "image": blog_data.image,
        "created_date": blog_data.created_at,
        "updated_date": blog_data.updated_at,
        "author": author
    }
    with get_mongo_db() as db:
        collection = db["blogs"]
        data_inserted_instance = collection.insert_one(blog)

        if data_inserted_instance.inserted_id:
            return {"message": "Blog created successfully"}

    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Failed to create blog")

@router.get("/all", response_model=List[dict], status_code=status.HTTP_200_OK)
def get_all_blogs(current_user: Annotated[UserModel, Depends(get_current_user)],
                  db:Database = Depends(get_mongo_db)):
    if current_user:
        with get_mongo_db() as db:
            blogs_collection = db["blogs"]
            projection = {
                'title':1,
                'content':0,
                'images':1,
                'created_at':1,
                'updated_at':0,
                'author':1,
                '_id':0
            }
            all_blogs = list(blogs_collection.find({}, projection))
            return {"blogs":all_blogs}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized to make this request"
    )

@router.get("/blog",  response_model=BlogResponse, status_code=status.HTTP_200_OK)
def get_individula_blog(
        request:Request,
        current_user: Annotated[UserModel, Depends(get_current_user)],
        db:Database=Depends(get_mongo_db)
    ):
    if current_user:
        blog_title = request.query_params.get("title").strip()
        if blog_title:
            with get_mongo_db() as db:
                blogs_collection = db["blogs"]
                blog_data = blogs_collection.find_one({"title":blog_title})
                if blog_data:
                    return BlogResponse(**blog_data)
                return {"message":"No data available"}
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title is required to get the blog data"
        )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized to make this request"
    )


