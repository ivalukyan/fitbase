from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from admin_app.routers.admin import router as admin_router
from admin_app.routers.auth import router as auth_router

app = FastAPI()
app.mount("/static", StaticFiles(directory="admin_app/static"), name="static")
api_router = APIRouter(
    prefix="/api",
    tags=["api"],
)

api_router.include_router(auth_router)
api_router.include_router(admin_router)

app.include_router(api_router)