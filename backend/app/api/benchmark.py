from fastapi import APIRouter
from app.models.benchmark import BenchmarkRequest, MetricsResult, BenchmarkResponse

router = APIRouter()

@router.get("/")
def get_router():
    return {"message" : "Running successfully"}

@router.post("/benchmark")
def benchmark(request: BenchmarkRequest):
    return {
        "message": "Input received",
        "data": request.model_dump()
    }