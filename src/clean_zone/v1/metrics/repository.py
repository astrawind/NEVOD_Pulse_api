from prometheus_client import Gauge

from src.metrics import MetricHolder
from src.clean_zone.v1.schemas import Parameter

metrics = MetricHolder()

class CZParametersMetrics:
    def __init__(self, holder = metrics):
        self._metrics = {"t_1" :Gauge('cz_parameters_temperature_room_1_celsius', 'Температура помещения 1', registry=holder.get_registry()),
                    "t_2" :Gauge('cz_parameters_temperature_room_2_celsius', 'Температура помещения 2', registry=holder.get_registry()),
                    "t_3" :Gauge('cz_parameters_temperature_room_3_celsius', 'Температура помещения 3', registry=holder.get_registry())}
        self.holder = holder

#    def __setattr__(self, name, value):
#        if name in self._metrics:
#            self._metrics[name].set(value)
#        else:
#            super().__setattr__(name, value)

    def put_metrics(self, metric_container: dict|None):
        if metric_container is None:
            for key in self._metrics:
                self._metrics[key].set(0)
        else:
            for key in metric_container:
                if key in self._metrics:
                    self._metrics[key].set(metric_container[key])

    def get_metrics(self):
        return self.holder.get_metrics()
    
clean_zone_metrics = CZParametersMetrics()