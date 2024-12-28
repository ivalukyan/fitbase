from fastapi import FastAPI, APIRouter
from admin_app.routers.admin import router as admin_router
from admin_app.routers.auth import router as auth_router

app = FastAPI()

api_router = APIRouter(
    prefix="/api",
    tags=["api"],
)

api_router.include_router(auth_router)
api_router.include_router(admin_router)

app.include_router(api_router)