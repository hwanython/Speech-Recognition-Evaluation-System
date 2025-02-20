from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up...")
    yield
    # Shutdown
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

# Static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Import routers
from app.routers import main_routes, evaluation, dataset_routes  # evaluation_routes를 evaluation으로 변경

# Include routers
app.include_router(main_routes.router)
app.include_router(evaluation.router, prefix="/evaluation", tags=["evaluation"])  # evaluation_routes를 evaluation으로 변경
app.include_router(dataset_routes.router, prefix="/dataset", tags=["dataset"]) 