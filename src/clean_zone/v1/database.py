from src.clean_zone.v1.config import settings
from src.database import PostresConnectionMaker

cz_connection_maker = PostresConnectionMaker(settings.CZ_POSTGRES_USERNAME, settings.CZ_POSTGRES_PASSWORD, settings.CZ_POSTGRES_HOST, settings.CZ_POSTGRES_PORT, settings.CZ_POSTGRES_DBNAME)
