from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.benchmark import router as benchmark_router
from app.database.database import engine,Base

from app.database.schemas import BenchmarkResult,BenchmarkRun

app = FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(benchmark_router)

app.add_middleware(
        CORSMiddleware,
        allow_origins="http://localhost:5173",
        allow_methods=["*"],
        allow_headers=["*"],
                   )