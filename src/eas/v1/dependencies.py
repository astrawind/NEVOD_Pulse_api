from .config import settings
from src.database import MongoConnectionMaker
from .repository import EASRepository
from src.metrics import GaugeManager, HistogramManager, MetricRegistry
from .metric_service import EASMetricService, EASMetricHistogramService
from fastapi import Depends
from src.metrics import MetricDefinition, HistogramMetricDefinition
from .utils import make_metric_definitions, get_eas_metric_alias

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
    metrics_definitions = make_metric_definitions([
        (('quality_rate', 'persents'), '{Number of "good" events} / {number of all events}', ('cluster'))
    ])
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
    
def create_histogram_manager(registry: MetricRegistry = Depends(create_metric_registry)) -> HistogramManager:
    metrics_definitions = [HistogramMetricDefinition(alias = 'q_distribution', name = 'eas_q_distribution_coulombs', description = 'distributions of charge in eas', labels = ('cluster', 'ds'), buckets = list(range(51)))]
    return HistogramManager(metrics_definitions, registry)

def create_histogram_metric_service(
    repo: EASRepository = Depends(create_repository),
    hist: HistogramManager = Depends(create_histogram_manager)
) -> EASMetricHistogramService:
    return EASMetricHistogramService(
        db=repo,
        metric=hist,
    )