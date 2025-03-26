from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class HVChan(BaseModel):
    hv_chan: str = Field(..., alias='HVchan')
    temp: int = Field(..., alias='Temp')
    hv_max: float = Field(..., alias='HVmax')
    v_mon: float = Field(..., alias='Vmon')
    i_mon: float = Field(..., alias='Imon')
    v0_set: int = Field(..., alias='V0set')
    i0_set: int = Field(..., alias='I0set')
    en_ex: str = Field(..., alias='EnEx')
    pw: str = Field(..., alias='Pw')
    status: str = Field(..., alias='Status')
    sv_max: int = Field(..., alias='SVmax')
    rup: int = Field(..., alias='Rup') 
    rdwn: int = Field(..., alias='Rdwn')
    trip: str = Field(..., alias='Trip')
    pon: str = Field(..., alias='Pon')
    pdwn: str = Field(..., alias='Pdwn')  

class HVItem(BaseModel):
    time: datetime
    step: str = Field(...)
    chans: list[HVChan]



