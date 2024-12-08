from fastapi import APIRouter, Depends, HTTPException
from src.clean_zone.v1.repository import ParameterRepository
from src.clean_zone.v1.schemas import Parameter, TimeRange, ParameterData

router = APIRouter(
    prefix="/clean_zone/v1/data",
    tags=["Чистая зона"],
)

@router.get("/parameters/{parameter_id}", description="Получение параметров с определенным id из таблицы Parameters")
async def get_parameter(parameter_id: int) -> Parameter:
    param = ParameterRepository.get_parameter(parameter_id)
    if param:
        return param
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@router.get("/parameters", description="Получение значений таблицы Parameters за определенный промежуток времени")
async def get_paraeters(timeline: TimeRange = Depends()) -> list[Parameter]:
    params = ParameterRepository.get_parameters(timeline)
    return params

@router.get("/paramerers/avg", description="Получение средних значений таблицы Parameters за интересующий промежуток времени")
async def get_paraeters(timeline: TimeRange = Depends()) -> ParameterData:
    params = ParameterRepository.get_avg_parameters(timeline)
    return params

@router.get("/paramerers/max", description="Получение максимальных значений таблицы Parameters за интересующий промежуток времени")
async def get_paraeters(timeline: TimeRange = Depends()) -> ParameterData:
    params = ParameterRepository.get_max_parameters(timeline)
    return params

@router.get("/paramerers/min", description="Получение минимальных значений таблицы Parameters за интересующий промежуток времени")
async def get_paraeters(timeline: TimeRange = Depends()) -> ParameterData:
    params = ParameterRepository.get_min_parameters(timeline)
    return params