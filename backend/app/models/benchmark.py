from pydantic import BaseModel
from typing import Literal


class BenchmarkRequest(BaseModel):
    url: str
    method: Literal["GET", "POST", "PUT", "DELETE"]
    requests: int
    concurrency: int


class MetricsResult(BaseModel):
    average_latency: float
    min_latency: float
    max_latency: float
    success_rate: float


class BenchmarkResponse(BaseModel):
    message: str
    metrics: MetricsResult