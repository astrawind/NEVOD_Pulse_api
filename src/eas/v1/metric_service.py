from src.metrics import GaugeManager, MetricService
from src.schemas import Metric
from .repository import EASRepository
from .utils import get_eas_metric_alias
from .config import settings
from datetime import datetime, timedelta

def make_metric(metric_name, units, cluser, value) -> Metric:
    return Metric(
        name=get_eas_metric_alias(metric_name, units),
        labels=(cluser,),
        value=value
        )

class EASMetricService(MetricService):
    
    def __init__(self, db: EASRepository, metric: GaugeManager, time_delay: int):
        super().__init__(metric)
        self._db: EASRepository = db
        self.time_delay = time_delay
        
    def collect_last_metrics(self) -> list[Metric]:
        quality_rates = self.db.get_quality_rate(datetime.now() - timedelta(seconds=self.time_delay))
        quality_metrics = [make_metric('quality_rate', 'persents', rate["cluster"], rate["value"]) for rate in quality_rates]
        return quality_metrics
    
    