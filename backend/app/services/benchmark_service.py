from app.services.load_generator import generate_requests
from app.services.async_load_generator import async_call_generate
from app.services.metrics_service import metrics_calculator, calculate_percentile


async def run_benchmark(request):
    results,duration,rps = await async_call_generate(
        request.total_requests,
        request.url,
        request.concurrency
    )

    latency = []
    for latencies in results:
        latency_ms = latencies['latency_ms']
        latency.append(latency_ms)

    p50 = calculate_percentile(latency,50)
    p90 = calculate_percentile(latency,90)
    p95 = calculate_percentile(latency,95)
    p99 = calculate_percentile(latency,99)

    metrics,codes = metrics_calculator(results,p50,p90,p95,p99)

    return {
        "benchmark": {
            "url": request.url,
            "total_requests": request.total_requests,
            "concurrency" : request.concurrency,
            "duration_ms" : round(duration,2),
            "requests_per_sec" : round(rps,2)
        },
        "response_distribution" : codes,
        "metrics": metrics,
        "results": results
    }