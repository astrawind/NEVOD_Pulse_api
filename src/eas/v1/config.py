from src.schemas import Settings

class EASSettings(Settings):
    EAS_MONGO_USERNAME: str
    EAS_MONGO_PASSWORD: str
    EAS_MONGO_HOST: str
    EAS_MONGO_PORT: int
    EAS_MONGO_DBNAME: str
    EAS_POOL_SIZE: int
    EAS_DELAY: int

settings = EASSettings()