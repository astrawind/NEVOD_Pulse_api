from fastapi import APIRouter, Depends
from src.clean_zone.v1.repository import ParameterRepository
from src.clean_zone.v1.schemas import Parameter, TimeRange, ParameterData

router = APIRouter(
    prefix="/clean_zone/v1/data",
    tags=["Чистая зона"],
)

@router.get("/parameters/{parameter_id}")
async def get_parameter(parameter_id: int) -> Parameter:
    pass

@router.get("/parameters")
async def get_paraeters(timeline: TimeRange = Depends()) -> list[Parameter]:
    params = ParameterRepository.get_parameters(timeline)
    return params

@router.get("/paramerers/avg")
async def get_paraeters(timeline: TimeRange = Depends()) -> ParameterData:
    params = ParameterRepository.get_avg_parameters(timeline)
    return params