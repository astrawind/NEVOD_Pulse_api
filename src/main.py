from fastapi import FastAPI

from src.clean_zone.v1.data.router import router as cz_router
from src.clean_zone.v1.metrics.router import router as cz_metric_router
from src.hv.v1.router import router as hv_metric_router
from src.eas.v1.router import router as eas_metric_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="NEVOD Pulse",
        version="1.0",
        description="API для установок НОЦ НЕВОД",
        docs_url="/docs",
    )
    app.include_router(cz_router)
    app.include_router(cz_metric_router)
    app.include_router(hv_metric_router)
    app.include_router(eas_metric_router)
    return app