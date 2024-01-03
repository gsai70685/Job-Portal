from fastapi import FastAPI
from routers import auth, reg_admin_hr, jobs_crud, blogs
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    'http://localhost:5173'
]

# middleware declaration
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Use `include_router` to include the router in your FastAPI app
app.include_router(auth.router, tags=["Authentication"])
app.include_router(jobs_crud.router, tags=["Jobs Data"], prefix="/jobs")
app.include_router(reg_admin_hr.router, tags=["AdminAuth"], prefix="/register")
app.include_router(blogs.router, tags=["Blogs"], prefix="/blog")

if __name__ == "__main__":
    # Specify the module and app instance for uvicorn to run
    import uvicorn

    # Specify the module (main) and app instance (app) for uvicorn to run
    uvicorn.run("main:app", host="127.0.0.1", port=8000)


def hello():
    pass

print("Hello")
