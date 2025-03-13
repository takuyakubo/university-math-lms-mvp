from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, problems, tags, progress

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(problems.router, prefix="/problems", tags=["problems"])
api_router.include_router(tags.router, prefix="/tags", tags=["tags"])
api_router.include_router(progress.router, prefix="/progress", tags=["progress"])