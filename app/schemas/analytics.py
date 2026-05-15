from pydantic import BaseModel


class MetricsStats(BaseModel):
    min: float | None
    max: float | None
    count: int
    sum: float
    median: float | None


class AnalysticResult(BaseModel):
    x_stats: MetricsStats
    y_stats: MetricsStats
    z_stats: MetricsStats

