from src.schemas import Settings

class ApiSettings(Settings):
    CZ_POSTGRES_USERNAME: str
    CZ_POSTGRES_PASSWORD: str
    CZ_POSTGRES_HOST: str
    CZ_POSTGRES_PORT: int
    CZ_POSTGRES_DBNAME: str

settings = ApiSettings()