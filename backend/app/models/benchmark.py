from pydantic import BaseModel
from typing import Literal


class BenchmarkRequest(BaseModel):
    url: str
    total_requests: int
    timeout: int = 15


class MetricsResult(BaseModel):
    total_requests : float
    successful_requests : float
    failed_requests : float
    success_rate : float
    failure_rate : float
    average_latency: float
    min_latency: float
    max_latency: float


class BenchmarkResponse(BaseModel):
    message: str
    metrics: MetricsResult