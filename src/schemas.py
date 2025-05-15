from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, BaseModel


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

class MetricDefinition(BaseModel):
    name: str = Field(...)
    description: str = Field(default='')
    labels: tuple[str] = Field(default=tuple())

class Metric(BaseModel):
    name: str = Field(...)
    labels: tuple[str] = Field(default=tuple())
    value: float|int = Field()