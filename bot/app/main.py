from fastapi import FastAPI, APIRouter, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from admin_app.routers.admin import router as admin_router
from admin_app.routers.auth import router as auth_router

app = FastAPI()
app.mount("/static", StaticFiles(directory="admin_app/static"), name="static")
api_router = APIRouter(
    prefix="/api",
    tags=["api"],
)

templates = Jinja2Templates("admin_app/templates")

@app.exception_handler(404)
async def custom_404_handler(request: Request, exp: HTTPException):
    return templates.TemplateResponse("errors.html", {"request": request, 'status': exp.status_code,
                                                      'details': exp.detail})


@app.exception_handler(500)
async def custom_500_handler(request: Request, exp: HTTPException):
    return templates.TemplateResponse("errors.html", {"request": request, 'status': exp.status_code,
                                                      'details': exp.detail})


@app.exception_handler(400)
async def custom_400_handler(request: Request, exp: HTTPException):
    return templates.TemplateResponse("errors.html", {"request": request, 'status': exp.status_code,
                                                      'details': exp.detail})

api_router.include_router(auth_router)
api_router.include_router(admin_router)

app.include_router(api_router)