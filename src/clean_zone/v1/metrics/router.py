from fastapi import APIRouter, Depends, HTTPException
from src.clean_zone.v1.repository import ParameterRepository
from src.clean_zone.v1.schemas import Parameter, TimeRange, ParameterData, Pagination
from datetime import datetime, timedelta
from .repository import clean_zone_metrics
from prometheus_client import CONTENT_TYPE_LATEST
from fastapi.responses import Response

router = APIRouter(
    prefix="/clean_zone/v1/metrics",
    tags=["Метрики"],
)

@router.get("/", description="Получение метрик")
async def get_parameter():
    page = Pagination(page=0, limit=3)
    scrape_time = datetime.now()
    scrape_time = scrape_time.replace(year=scrape_time.year - 1)
    time = TimeRange(start = scrape_time - timedelta(minutes=1), end = scrape_time)
    parameters = ParameterRepository.get_parameters(time, page)
    clean_zone_metrics.put_metrics(None if not parameters else parameters[-1].model_dump())
    return Response(content=clean_zone_metrics.get_metrics(), media_type=CONTENT_TYPE_LATEST)