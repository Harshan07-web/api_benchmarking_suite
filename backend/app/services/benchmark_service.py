from app.services.load_generator import generate_requests
from app.services.async_load_generator import async_call_generate
from app.services.metrics_service import metrics_calculator, calculate_percentile
from app.repository.benchmark_repository import save_benchmark_results,save_benchmark_run

async def run_benchmark(request, db):
    results, duration, rps = await async_call_generate(
        no_of_requests=request.total_requests,
        url=str(request.url),
        concurrency=request.concurrency,
    )

    latencies = [
        result["latency_ms"]
        for result in results
        if result["latency_ms"] is not None
    ]

    median = calculate_percentile(latencies, 50)
    p90 = calculate_percentile(latencies, 90)
    p95 = calculate_percentile(latencies, 95)
    p99 = calculate_percentile(latencies, 99)

    metrics, response_distribution = metrics_calculator(
        results,
        median,
        p90,
        p95,
        p99,
    )

    benchmark_run = save_benchmark_run(
        db=db,
        request=request,
        duration_ms=round(duration, 2),
        requests_per_second=round(rps, 2),
        metrics=metrics,
    )

    save_benchmark_results(
        db=db,
        benchmark_run_id=benchmark_run.id,
        results=results,
    )

    return {
        "benchmark": {
            "benchmark_name": request.benchmark_name,
            "url": str(request.url),
            "method": request.method,
            "total_requests": request.total_requests,
            "concurrency": request.concurrency,
            "duration_ms": round(duration, 2),
            "requests_per_second": round(rps, 2),
        },
        "response_distribution": response_distribution,
        "metrics": metrics,
        "results": results,
    }