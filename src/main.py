from fastapi import FastAPI

from src.clean_zone.v1.data.router import router as cz_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="NEVOD Pulse",
        version="1.0",
        description="API для установок НОЦ НЕВОД",
        docs_url="/",
    )
    app.include_router(cz_router)
    return app