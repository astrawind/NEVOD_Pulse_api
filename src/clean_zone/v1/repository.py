from sqlalchemy import select
from sqlalchemy.sql import func
from typing import Callable, Generator

from .database import cz_connection_maker as get_connection
from .schemas import Parameter, TimeRange, ParameterData
from .models import Parameter as ParameterOrm

class ParameterRepository:
    
    @classmethod
    def get_parameters(cls, timeline: TimeRange, get_conn: Generator = get_connection) -> list[Parameter]:
        with get_conn() as conn:
            query = select(ParameterOrm).where(ParameterOrm.date_time.between(timeline.start, timeline.end))
            result = conn.execute(query)
            parameters = result.scalars().all()
            res_params = [Parameter.model_validate(param.model_dump()) for param in parameters]
            return res_params
        
    @classmethod
    def get_parameter(cls, id: int, get_conn: Generator = get_connection)->Parameter:
        with get_conn() as conn:
            query = select(ParameterOrm).where(ParameterOrm.order_id == id)
            result = conn.execute(query)
            parameter = result.scalars().one()
            res_param = Parameter.model_validate(parameter.model_dump())
            return res_param
        
    @classmethod
    def get_agregation(cls, timeline: TimeRange, func: Callable, get_conn = get_connection)->ParameterData:
        with get_conn() as conn:
            query = select(func(ParameterOrm.t_out).label("t_out"),
                            func(ParameterOrm.t_intake).label("t_intake"),
                            func(ParameterOrm.h_intake).label("h_intake"),
                            func(ParameterOrm.t_water).label("t_water"),
                            func(ParameterOrm.t_mixer).label("t_mixer"),
                            func(ParameterOrm.t_1).label("t_1"),
                            func(ParameterOrm.t_2).label("t_2"),
                            func(ParameterOrm.t_3).label("t_3"),
                            func(ParameterOrm.t_4).label("t_4"),
                            func(ParameterOrm.r_gate).label("r_gate"),
                            func(ParameterOrm.r_heater).label("r_heater"),
                            func(ParameterOrm.v_intake).label("v_intake"),
                            func(ParameterOrm.v_exhaust).label("v_exhaust"),
                            func(ParameterOrm.heater_setup).label("heater_setup"),
                            func(ParameterOrm.t_average).label("t_average"),
                            ).where(ParameterOrm.date_time
                                    .between(timeline.start, timeline.end))
            result = conn.execute(query)
            parameter = result.fetchone()
            res_param = ParameterData.model_validate({column: value for column, value in zip(result.keys(), parameter)})
            return res_param
        
    @classmethod
    def get_avg_parameters(cls, timeline: TimeRange, get_conn = get_connection)->ParameterData:
        res_param = ParameterRepository.get_agregation(timeline, func.avg)
        return res_param

    @classmethod
    def get_min_parameters(cls, timeline: TimeRange, get_conn = get_connection)->ParameterData:
        res_param = ParameterRepository.get_agregation(timeline, func.min)
        return res_param
    
    @classmethod
    def get_max_parameters(cls, timeline: TimeRange, get_conn = get_connection)->ParameterData:
        res_param = ParameterRepository.get_agregation(timeline, func.max)
        return res_param
