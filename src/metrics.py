from prometheus_client import generate_latest, CollectorRegistry

class MetricHolder():

    def __init__(self):
        self.registry = CollectorRegistry()

    def get_registry(self):
        return self.registry
    
    def get_metrics(self):
        return generate_latest(self.registry)