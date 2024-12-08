
from datetime import datetime

from sqlmodel import Field, SQLModel

class Parameter(SQLModel, table=True):
    __tablename__ = "parameters"
    order_id: int = Field(primary_key=True)
    date_time: datetime = Field(default=None, index=True)
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

class State(SQLModel, table=True):
    __tablename__ = "states"
    order_id: int = Field(primary_key=True)
    date_time: datetime = Field(default=None, index=True)
    fault: str = Field(default=None)
    intake_fan: str = Field(default=None)
    intake_fan_converter: float = Field(default=None)
    intake_fan_thermal_protection: float = Field(default=None)
    intake_fan_overpressure: float = Field(default=None)
    exhaust_fan: float = Field(default=None)
    exhaust_fan_converter: float = Field(default=None)
    exhaust_fan_thermal_protection: float = Field(default=None)
    exhaust_fan_overpressure: float = Field(default=None)
    compressor_fault: float = Field(default=None)
    compressor_1st_stage: float = Field(default=None)
    compressor_2nd_stage: float = Field(default=None)
    intake_filter_1_pollution: float = Field(default=None)
    intake_filter_2_pollution: float = Field(default=None)
    switch_auto: float = Field(default=None)
    switch_manual: float = Field(default=None)
    heater_thermal_contact: float = Field(default=None)
    capillary_thermostat: float = Field(default=None)
    fire_alarm: float = Field(default=None)
    pump: float = Field(default=None)
    pump_protection: float = Field(default=None)
    humidifier_fault: float = Field(default=None)
    humidifier: float = Field(default=None)
