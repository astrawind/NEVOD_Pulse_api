from .config import settings
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta
from prometheus_client import CONTENT_TYPE_LATEST
from fastapi.responses import Response
from .dependencies import create_metric_service
from .metric_service import EASMetricService

router = APIRouter(
    prefix="/eas/v1/metrics",
    tags=["Метрики", "eas"],
)

@router.get("/", description="Получение метрик")
async def get_eas_metrics(
    service: EASMetricService = Depends(create_metric_service)
):
    service.update_last_metrics()
    return Response(content=service.get_last_metrics(), media_type=CONTENT_TYPE_LATEST)