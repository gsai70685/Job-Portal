from fastapi import FastAPI
from routers import auth, jobs_crud, blogs
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:5173"
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Content-Type","Set-Cookie"]
)

# Use `include_router` to include the router in your FastAPI app
app.include_router(auth.router, tags=["Authentication"])
app.include_router(jobs_crud.router, tags=["Jobs Data"], prefix="/jobs")
app.include_router(blogs.router, tags=["Blogs"], prefix="/blogs")

if __name__ == "__main__":
    # Specify the module and app instance for uvicorn to run
    import uvicorn

    # Specify the module (main) and app instance (app) for uvicorn to run
    uvicorn.run(host="127.0.0.1", port=8000)
