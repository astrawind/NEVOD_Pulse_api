from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, BaseModel


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore', override=True)

class MetricDefinition(BaseModel):
    alias: str = Field(...)
    name: str = Field(...)
    description: str = Field(default='')
    labels: tuple[str] = Field(default=tuple())

class Metric(BaseModel):
    alias: str = Field(...)
    labels: tuple = Field(default=tuple())
    value: float|int = Field()
    
class HistogramMetricDefinition(MetricDefinition):
    buckets: list[float]