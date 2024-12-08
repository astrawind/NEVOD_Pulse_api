from sqlalchemy import select

from .database import cz_connection_maker as get_connection
from .schemas import Parameter, TimeRange
from .models import Parameter as ParameterOrm

# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

class ParameterRepository:
    
    @classmethod
    def get_parameters(cls, timeline: TimeRange, get_conn = get_connection) -> list[Parameter]:
        # if any(timeline.start, timeline.end):
        with get_conn() as conn:
            query = select(ParameterOrm).where(ParameterOrm.date_time > timeline.start)
            result = conn.execute(query)
            parameters = result.scalars().all()
            res_params = [Parameter.model_validate(param.model_dump()) for param in parameters]
            return res_params
        
    @classmethod
    def get_parameter(cls, )

