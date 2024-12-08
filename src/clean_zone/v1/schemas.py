from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class TimeRange(BaseModel):
    start: Optional[datetime] = Field(..., default=datetime(1970, 1, 1), description="Дата и время начала интересующего периода времени в формате YYYY-MM-DD HH:MM:SS") #Default - Linux low date value
    end: Optional[datetime] = Field(..., default_factory=datetime.now, description="Дата и время конца интересующего периода времени в формате YYYY-MM-DD HH:MM:SS")

class Page(BaseModel):
    page: Optional[int] = Field(..., default=0, description="Номер интересующей страницы")
    limit: int = Field(..., description="Количество записей на каждой странице")

class ParameterData(BaseModel):
    t_out: float = Field(..., description="Наружная температура в °C")
    t_intake: float = Field(..., description="Температура приточного воздуха в °C")
    h_intake: float = Field(..., description="Влажность приточного воздуха в %")
    t_water: float = Field(..., description="Температура обратной воды в °C")
    t_mixer: float = Field(..., description="Температура в камере смешения в °C")
    t_1: float = Field(..., description="Температура помещения 1 в °C")
    t_2: float = Field(..., description="Температура помещения 2 в °C")
    t_3: float = Field(..., description="Температура помещения 3 в °C")
    t_4: float = Field(..., description="Температура помещения 4 в °C")
    r_gate: float = Field(..., description="Процент открытия заслонок в %")
    r_heater: float = Field(..., description="Процент открытия клапана нагрева в %")
    v_intake: float = Field(..., description="Скорость приточного вентилятора в %")
    v_exhaust: float = Field(..., description="Скорость вытяжного вентилятора в %")
    heater_setup: float = Field(..., description="Задание эл. нагревателю в %")
    t_average: float = Field(..., description="Средняя температура в помещении в °C")

class Parameter(ParameterData):
    order_id: int = Field(..., description="id записи")
    date_time: datetime = Field(..., description="Дата и время измерения в формате YYYY-MM-DD HH:MM:SS")

