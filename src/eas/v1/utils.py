from src.metrics import MetricDefinition

def get_eas_metric_alias(metric_name, units):
    return f'eas_{metric_name}_{units}'

def make_metric_definitions(container: list[tuple]) -> list[MetricDefinition]:
    return [MetricDefinition(alias=metric_name, name=get_eas_metric_alias(metric_name, units), description=description, labels=(labels,))
            for (metric_name, units), description, labels in container]