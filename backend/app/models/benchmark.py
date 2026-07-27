from typing import Literal
from pydantic import BaseModel, HttpUrl


class BenchmarkRequest(BaseModel):
    benchmark_name: str | None = None
    url: HttpUrl
    method: Literal["GET", "POST"] = "GET"
    total_requests: int
    concurrency: int = 10
    timeout: int = 15


class BenchmarkInfo(BaseModel):
    url: HttpUrl
    method: str
    total_requests: int
    concurrency: int
    duration_ms: float
    requests_per_second: float


class MetricsResult(BaseModel):
    successful_requests: int
    failed_requests: int
    success_rate: float
    failure_rate: float
    average_latency: float
    median_latency: float
    p90_latency: float
    p95_latency: float
    p99_latency: float
    minimum_latency: float
    maximum_latency: float


class RequestResult(BaseModel):
    status_code: int | None
    latency_ms: float | None
    success: bool
    error: str | None


class BenchmarkResponse(BaseModel):
    benchmark: BenchmarkInfo
    response_distribution: dict[int, int]
    metrics: MetricsResult
    results: list[RequestResult]