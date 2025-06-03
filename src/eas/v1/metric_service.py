from src.metrics import GaugeManager, MetricService, HistogramManager
from src.schemas import Metric
from .repository import EASRepository
from .utils import get_eas_metric_alias
from .config import settings
from datetime import datetime, timedelta
import numpy as np

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

def make_hist_metric(metric_name, cluster, ds, bucket, value):
    return Metric(
        alias=metric_name,
        labels=(cluster, ds, bucket),
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
        if container is not None:
            result = [make_metric(metric_name, rate["cluster"], rate["value"]) for rate in container]
        else:
            result = None
        return result
    
class EASMetricHistogramService(MetricService):
    
    def __init__(self, db: EASRepository, metric: GaugeManager):
        super().__init__(metric)
        self._db: EASRepository = db
        
    def collect_last_metrics(self) -> list[Metric]:
        q_values = self._db.get_q_std_values(datetime.now())
        charge_metrics = self._prepare_metric('q_distribution', q_values)
        return charge_metrics
    
    def _prepare_metric(self, metric_name, container):
        round_number = 2
        bin_width = 1
        min_x = 0
        max_x = 50
        if container is not None:
            result = list()
            for q_valuses in container:
                cluster = q_valuses['cluster']
                ds = q_valuses['ds']
                hist, x = np.histogram(q_valuses['values'], np.arange(min_x - 0.5 * bin_width, max_x + 0.5 * bin_width + bin_width, bin_width))
                bins = [round(0.5 * (x[i] + x[i + 1]), round_number) for i in range(len(hist))]
                result.extend([make_hist_metric(metric_name, cluster, ds, bucket, value) for value, bucket in zip(hist, bins[:-1])])
        else:
            result = None
        return result
    