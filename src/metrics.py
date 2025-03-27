from prometheus_client import generate_latest, CollectorRegistry, Gauge

class MetricHolder():

    def __init__(self):
        self.registry = CollectorRegistry()

    def get_registry(self):
        return self.registry
    
    def get_metrics(self):
        return generate_latest(self.registry)
    
class GaugeMetricCollector:
    def __init__(self, metrics: list[tuple], metric_holder: MetricHolder=None):
        if metric_holder is None:
            self._holder = MetricHolder()
        elif metric_holder.isinstance(MetricHolder):
            self._holder = metric_holder
        else:
            raise TypeError('wrong registry type')
        self._metrics = self._create_gauges(metrics)
        
    def _create_gauges(self, metrics):
        """Инициализирует и возвращает словарь метрик."""
        return {
            alias: Gauge(
                name=metric_name,
                documentation=metric_description,
                registry=self._holder.get_registry()
            )
            for alias, metric_name, metric_description in metrics
        }

    def put_metrics(self, metric_container: dict|None):
        if metric_container is None:
            for key in self._metrics:
                self._metrics[key].set(0)
        else:
            for key in metric_container:
                if key in self._metrics:
                    self._metrics[key].set(metric_container[key])

    def get_metrics(self):
        return self._holder.get_metrics()