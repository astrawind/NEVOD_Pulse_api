from src.metrics import GaugeMetricCollector
from .infrastructure import HVHandler
from datetime import datetime, timedelta
from .config import settings
from .utils import make_unique_metric_alias

class HVMetricService:
    def __init__(self, metric_collector, controller):
        self._collector: GaugeMetricCollector = metric_collector
        self._controller: HVHandler = controller
        
    def collect_last_metrics(self) -> dict:
        last_record = self._controller.get_last_record(datetime.utcnow().date())
        if False and (last_record is None or (datetime.utcnow() - last_record.time > timedelta(seconds=settings.HV_STEP))):
            return None
        result = dict()
        for chan in last_record.chans:
            chan_dict = chan.model_dump(by_alias=True)
            chan_name = chan_dict['HVchan']
            for atr_name in chan_dict:
                if atr_name == 'HVchan':
                    continue
                result[make_unique_metric_alias(chan_name, atr_name)] = chan_dict[atr_name]
        return result
    
    def process_metrics(self, metrics: dict):
        self._collector.put_metrics(metrics)
        
    def update_last_metrics(self):
        metrics = self.collect_last_metrics()
        self.process_metrics(metrics)
        
    def get_last_metrics(self):
        return self._collector.get_metrics()