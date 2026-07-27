from datetime import datetime,UTC

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.database.database import Base


class BenchmarkRun(Base):
    __tablename__ = "benchmark_runs"

    id = Column(Integer, primary_key=True, autoincrement=True)

    benchmark_name = Column(String(255), nullable=True)
    url = Column(String(500), nullable=False, index=True)
    http_method = Column(String(20), nullable=False)

    total_requests = Column(Integer, nullable=False)
    concurrency = Column(Integer, nullable=False)
    timeout_seconds = Column(Integer, nullable=False)

    duration_ms = Column(Float, nullable=False)
    requests_per_second = Column(Float, nullable=False)

    successful_requests = Column(Integer, default=0, nullable=False)
    failed_requests = Column(Integer, default=0, nullable=False)
    success_rate = Column(Float, nullable=False)
    failure_rate = Column(Float, nullable=False)

    average_latency = Column(Float, nullable=False)
    median_latency = Column(Float, nullable=False)
    p90_latency = Column(Float, nullable=False)
    p95_latency = Column(Float, nullable=False)
    p99_latency = Column(Float, nullable=False)
    minimum_latency = Column(Float, nullable=False)
    maximum_latency = Column(Float, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
        index=True,
    )

    results = relationship(
        "BenchmarkResult",
        back_populates="benchmark",
        cascade="all, delete-orphan",
    )


class BenchmarkResult(Base):
    __tablename__ = "benchmark_results"

    id = Column(Integer, primary_key=True, autoincrement=True)

    benchmark_run_id = Column(
        Integer,
        ForeignKey("benchmark_runs.id"),
        nullable=False,
    )

    status_code = Column(Integer, nullable=True)
    latency_ms = Column(Float, nullable=True)
    success = Column(Boolean, nullable=False)
    error_message = Column(String(500), nullable=True)

    benchmark = relationship(
        "BenchmarkRun",
        back_populates="results",
    )