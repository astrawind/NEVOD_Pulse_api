
from datetime import datetime

from sqlmodel import Field, SQLModel, create_engine

class Parameter(SQLModel, table=True):
    order_id: int = Field(primary_key=True)
    date_time: datetime = Field(default=None)
    t_out: float= Field(default=None)
    t_intake: float= Field(default=None)
    h_intake: float= Field(default=None)
    t_water: float= Field(default=None)
    t_mixer: float= Field(default=None)
    t_1: float= Field(default=None)
    t_2: float= Field(default=None)
    t_3: float= Field(default=None)
    t_4: float= Field(default=None)
    r_gate: float= Field(default=None)
    r_heater: float= Field(default=None)
    v_intake: float= Field(default=None)
    v_exhaust: float= Field(default=None)
    heater_setup: float= Field(default=None)
    t_average: float= Field(default=None)

