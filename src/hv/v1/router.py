from .metric_service import HVMetricService
from .metric_controller import HVMetricCollector
from .infrastructure import HVHandler
from .config import settings
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta
from prometheus_client import CONTENT_TYPE_LATEST
from fastapi.responses import Response


router = APIRouter(
    prefix="/high_voltage/v1/metrics",
    tags=["Метрики", "hv"],
)

files_handler = HVHandler(settings.HV_DIRECTORY)
metric_collector = HVMetricCollector(["Uragan01", "Uragan02", "Uragan03", "Uragan04", "DECOR00-03", "DECOR12-15", "DECOR04", "DECOR08"],
                                     ["Vmon", "Imon", "V0set", "I0set"], ["volt", "ampere", "volt", "ampere"])
service = HVMetricService(metric_collector, files_handler)

@router.get("/", description="Получение метрик")
async def get_high_voltage_metrics():
    service.update_last_metrics()
    return Response(content=service.get_last_metrics(), media_type=CONTENT_TYPE_LATEST)