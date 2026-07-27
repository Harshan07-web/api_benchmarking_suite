from sqlalchemy.orm import Session

from app.database.schemas import BenchmarkRun, BenchmarkResult


def save_benchmark_run(
    db: Session,
    request,
    duration_ms: float,
    requests_per_second: float,
    metrics: dict,
):
    try:
        run = BenchmarkRun(
            benchmark_name=request.benchmark_name,
            url=str(request.url),
            http_method=request.method,
            total_requests=request.total_requests,
            concurrency=request.concurrency,
            timeout_seconds=request.timeout,
            duration_ms=duration_ms,
            requests_per_second=requests_per_second,
            successful_requests=metrics["successful_requests"],
            failed_requests=metrics["failed_requests"],
            success_rate=metrics["success_rate"],
            failure_rate=metrics["failure_rate"],
            average_latency=metrics["average_latency"],
            median_latency=metrics["median_latency"],
            p90_latency=metrics["p90_latency"],
            p95_latency=metrics["p95_latency"],
            p99_latency=metrics["p99_latency"],
            minimum_latency=metrics["minimum_latency"],
            maximum_latency=metrics["maximum_latency"],
        )

        db.add(run)
        db.commit()
        db.refresh(run)

        return run

    except Exception:
        db.rollback()
        raise


def save_benchmark_results(
    db: Session,
    benchmark_run_id: int,
    results: list,
):
    try:
        benchmark_results = []

        for result in results:
            benchmark_results.append(
                BenchmarkResult(
                    benchmark_run_id=benchmark_run_id,
                    status_code=result["status_code"],
                    latency_ms=result["latency_ms"],
                    success=result["success"],
                    error_message=result["error"],
                )
            )

        db.add_all(benchmark_results)
        db.commit()

        return benchmark_results

    except Exception:
        db.rollback()
        raise


def get_benchmark(db: Session, benchmark_id: int):
    return (
        db.query(BenchmarkRun)
        .filter(BenchmarkRun.id == benchmark_id)
        .first()
    )


def get_all_benchmarks(db: Session):
    return (
        db.query(BenchmarkRun)
        .order_by(BenchmarkRun.created_at.desc())
        .all()
    )


def delete_benchmark(db: Session, benchmark_id: int):
    benchmark = (
        db.query(BenchmarkRun)
        .filter(BenchmarkRun.id == benchmark_id)
        .first()
    )

    if benchmark is None:
        return None

    db.delete(benchmark)
    db.commit()

    return benchmark