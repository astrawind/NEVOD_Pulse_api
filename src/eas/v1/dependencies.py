from .config import settings
from src.database import MongoConnectionMaker
from .repository import EASRepository
from src.metrics import GaugeManager, MetricRegistry
from .metric_service import EASMetricService
from fastapi import Depends

connection_maker = MongoConnectionMaker(settings.EAS_MONGO_USERNAME,
                                        settings.EAS_MONGO_PASSWORD,
                                        settings.EAS_MONGO_HOST,
                                        settings.EAS_MONGO_PORT,
                                        settings.EAS_MONGO_DBNAME,
                                        settings.EAS_POOL_SIZE)
    
def create_repository() -> EASRepository:
    return EASRepository(connection_maker)

def create_metric_registry() -> MetricRegistry:
    return MetricRegistry()

def create_gauge_manager(registry: MetricRegistry = Depends(create_metric_registry)) -> GaugeManager:
    metrics_definitions = [
        ('quality_rate', 'persents', ['cluster'])
    ]
    return GaugeManager(metrics_definitions, registry)

def create_metric_service(
    repo: EASRepository = Depends(create_repository),
    gauge: GaugeManager = Depends(create_gauge_manager)
) -> EASMetricService:
    return EASMetricService(
        db=repo,
        metric=gauge,
        time_delay=settings.EAS_DELAY
    )