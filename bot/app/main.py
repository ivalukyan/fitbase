import sys

import uvicorn
import logging
from fastapi import FastAPI, APIRouter, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.responses import Response

from admin_app.routers.admin import router as admin_router
from admin_app.routers.auth import router as auth_router

app = FastAPI(version='1.5.0')
api_router = APIRouter(
    prefix="/api",
    tags=["Api"],
)

templates = Jinja2Templates("admin_app/templates")


# Обработчик для ошибки 404
@app.exception_handler(401)
async def custom_401_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse(
        "errors.html",
        {
            "request": request,
            "status": 401,
            "details": "Authentication credentials were not provided.",
        },
        status_code=401,
    )

# Обработчик для ошибки 404
@app.exception_handler(404)
async def custom_404_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse(
        "errors.html",
        {
            "request": request,
            "status": 404,
            "details": "Page not found"
        },
        status_code=404,
    )

# Обработчик для ошибки 500
@app.exception_handler(500)
async def custom_500_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse(
        "errors.html", {
            "request": request,
            "status": 500,
            "details": "Internal Server Error"},
        status_code=500,
    )

# Обработчик для ошибки 400
@app.exception_handler(400)
async def custom_400_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse(
        "errors.html",
        {
            "request": request,
            "status": 400,
            "details": "Bad Request"
        },
        status_code=400,
    )


api_router.include_router(auth_router)
api_router.include_router(admin_router)

app.include_router(api_router)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    uvicorn.run(app)
