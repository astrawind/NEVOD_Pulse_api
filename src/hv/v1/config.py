from src.schemas import Settings

class HVSettings(Settings):
    HV_DIRECTORY: str
    HV_STEP: int
    

settings = HVSettings()