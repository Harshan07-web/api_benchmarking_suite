from fastapi import APIRouter,Depends,HTTPException
from app.services.load_generator import generate_requests
from app.services.metrics_service import metrics_calculator
from app.services.benchmark_service import run_benchmark
from app.models.benchmark import BenchmarkRequest, MetricsResult, BenchmarkResponse
from app.database.database import SessionLocal,get_db
from app.database.schemas import BenchmarkRun,BenchmarkResult
from app.repository.benchmark_repository import get_benchmark,get_all_benchmarks
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/")
def get_router():
    return {"message" : "Running successfully"}

@router.post("/benchmark")
async def benchmark(request: BenchmarkRequest,db: Session=Depends(get_db)):
    return await run_benchmark(request=request,db=db)

# {
#   "url": "https://jsonplaceholder.typicode.com/posts",
#   "total_requests": 100,
#   "concurrency": 20,
#   "timeout": 15
# }

@router.get("/benchmark/all")
async def get_all_benchmark_info(db:Session=Depends(get_db)):
    return get_all_benchmarks(db)

@router.get("/benchmark/{id}")
async def get_benchmark_info(id:int,db:Session=Depends(get_db)):
    return get_benchmark(db,id)