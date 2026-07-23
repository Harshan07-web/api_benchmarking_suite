from fastapi import APIRouter
from app.services.load_generator import generate_requests
from app.services.metrics_service import metrics_calculator
from app.services.benchmark_service import run_benchmark
from app.models.benchmark import BenchmarkRequest, MetricsResult, BenchmarkResponse

router = APIRouter()

@router.get("/")
def get_router():
    return {"message" : "Running successfully"}

@router.post("/benchmark")
async def benchmark(request: BenchmarkRequest):
    return await run_benchmark(request=request)