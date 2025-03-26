from src.metrics import GaugeMetricCollector
from .utils import make_unique_metric_alias

class HVMetricCollector(GaugeMetricCollector):
    def __init__(self, channel_names, attributes, atributes_units, metric_holder = None):
        metrics = self._make_metric_pool(channel_names, attributes, atributes_units)
        super().__init__(metrics, metric_holder)
    
    def _make_metric_pool(channel_names, attributes, units):
        result = list()
        for chan in channel_names:
            chan = str(chan)
            for atribute, unit in zip(attributes, units): 
                result.append((make_unique_metric_alias(chan, atribute), f'hv_{chan.lower()}_{atribute.lower()}_{unit}'), '')
        return result
        