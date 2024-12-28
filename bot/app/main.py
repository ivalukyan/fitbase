from fastapi import FastAPI, APIRouter

app = FastAPI()

router = APIRouter(
    prefix="/api",
    tags=["api"]
)


@router.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(router)
