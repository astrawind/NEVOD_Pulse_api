from prometheus_client import generate_latest, CollectorRegistry, Gauge, Histogram
from abc import ABC, abstractmethod
from src.schemas import MetricDefinition, Metric

class MetricHolder():
    #depricated MetricRegistry

    def __init__(self):
        self.registry = CollectorRegistry()

    def get_registry(self):
        return self.registry
    
    def get_metrics(self):
        return generate_latest(self.registry)
    
class GaugeMetricCollector:
    #depricated MetricManager
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
    
class MetricRegistry():

    def __init__(self):
        self.registry = CollectorRegistry()

    def get_registry(self):
        return self.registry
    
    def get_metrics(self):
        return generate_latest(self.registry)
    
class MetricManager(ABC):
    
    def __init__(self, metrics_definitions: list[MetricDefinition], metric_registry: MetricRegistry | None = None):
        if metric_registry is None:
            self._holder = MetricRegistry()
        elif isinstance(metric_registry, MetricRegistry):
            self._holder = metric_registry
        else:
            raise TypeError('wrong registry type')
        
        self._metrics = self._create_metrics(metrics_definitions)
    
    @abstractmethod
    def _create_metrics(self, metrics_definitions: list[MetricDefinition]):
        pass
    
    @abstractmethod
    def put_metrics(self, metric_container: dict|None):
        pass
    
    def get_metrics(self):
        return self._holder.get_metrics()
    
    
    
class GaugeManager(MetricManager):
    
    def __init__(
        self, 
        metrics_definitions: list[MetricDefinition],
        metric_registry: MetricRegistry | None = None
        ):
        super().__init__(metrics_definitions, metric_registry)
        
    def _create_metrics(self, metrics_definitions):
        return self._create_gauges(metrics_definitions)
    
    def _create_gauges(self, metrics):
        print(metrics)
        return {
            metric.alias: Gauge(
                name=metric.name,
                documentation=metric.description,
                labelnames=metric.labels,
                registry=self._holder.get_registry()
            )
            for metric in metrics
        }

    def put_metrics(self, metric_container: list[Metric]|None):
        if not metric_container is None:
            for metric in metric_container:
                if metric.alias in self._metrics:
                    if metric.labels:
                        self._metrics[metric.alias].labels(*metric.labels).set(metric.value)
                    else:
                        self._metrics[metric.alias].set(metric.value)
                        
                        
class MetricService(ABC):
    def __init__(self, metric: MetricManager):
        self._metrics: GaugeManager = metric
        
    @abstractmethod
    def collect_last_metrics(self):
        pass
    
    def process_metrics(self, metrics: list[Metric]):
        self._metrics.put_metrics(metrics)
        
    def update_last_metrics(self):
        metrics = self.collect_last_metrics()
        self.process_metrics(metrics)
        
    def get_last_metrics(self):
        return self._metrics.get_metrics()