from fastapi import FastAPI

def create_app() -> FastAPI:
    app = FastAPI(
        title="NEVOD_Pulse",
        version="1.0",
        description="API для установок НОЦ НЕВОД",
        docs_url="/",
    )
    return app