from src.metrics import GaugeManager, MetricService
from src.schemas import Metric
from .repository import EASRepository
from .utils import get_eas_metric_alias
from .config import settings
from datetime import datetime, timedelta

def make_metric(metric_name, cluser, value) -> Metric:
    if cluser is None:
        return Metric(
            alias=metric_name,
            value=value
            )
    return Metric(
        alias=metric_name,
        labels=(cluser,),
        value=value
        )

class EASMetricService(MetricService):
    
    def __init__(self, db: EASRepository, metric: GaugeManager, time_delay: int):
        super().__init__(metric)
        self._db: EASRepository = db
        self.time_delay = time_delay
        
    def collect_last_metrics(self) -> list[Metric]:
        quality_rates = self._db.get_quality_rates(datetime.now() - timedelta(seconds=self.time_delay), datetime.now())
        quality_metrics = self._prepare_metric('quality_rate', quality_rates)
        return quality_metrics
    
    def _prepare_metric(self, metric_name, container):
        print(container)
        if container is None:
            result = [make_metric(metric_name, None, 0)]
        else:
            result = [make_metric(metric_name, rate["cluster"], rate["value"]) for rate in container]
        return result
    