from fastapi import APIRouter
from app.services.load_generator import generate_requests
from app.services.metrics_service import metrics_calculator
from app.models.benchmark import BenchmarkRequest, MetricsResult, BenchmarkResponse

router = APIRouter()

@router.get("/")
def get_router():
    return {"message" : "Running successfully"}

@router.post("/benchmark")
def benchmark(request: BenchmarkRequest):

    requests = generate_requests(request.total_requests,request.url,request.timeout)

    request_metrics = metrics_calculator(requests=requests)

    return {
        "metrics": request_metrics,
        "results" : requests
    }