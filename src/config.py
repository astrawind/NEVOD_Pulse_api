from src.models import Settings

class ApiSettings(Settings):
    API_HOST: str
    API_PORT: int

settings = ApiSettings()