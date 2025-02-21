from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from pathlib import Path
from app.config import settings  # settings 객체를 import


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up...")

    yield
    # Shutdown
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

# 기본 경로 설정
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

# 정적 파일 디렉토리 설정
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# processed 디렉토리를 직접 마운트
app.mount("/audio", StaticFiles(directory=str(settings.PROCESSED_DATA_DIR)), name="audio")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Import routers
from app.routers import main_routes, evaluation, dataset_routes  # evaluation_routes를 evaluation으로 변경

# Include routers
app.include_router(main_routes.router)
app.include_router(evaluation.router, prefix="/evaluation", tags=["evaluation"])  # evaluation_routes를 evaluation으로 변경
app.include_router(dataset_routes.router, prefix="/dataset", tags=["dataset"]) 