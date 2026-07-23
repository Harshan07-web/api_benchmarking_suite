from app.services.load_generator import generate_requests
from app.services.async_load_generator import async_call_generate
from app.services.metrics_service import metrics_calculator


async def run_benchmark(request):
    results,duration,rps = await async_call_generate(
        request.total_requests,
        request.url
    )

    metrics = metrics_calculator(results)

    return {
        "benchmark": {
            "url": request.url,
            "total_requests": request.total_requests,
            "duration" : round(duration,2),
            "rps" : round(rps,2)
        },
        "metrics": metrics,
        "results": results
    }