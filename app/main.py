
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.connection import init_db
from app.api import (
    health,
    predictions,
    sales,
    monitoring,
    alerts,
    models,
    retraining,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="SalesGuard AI API",
    description=(
        "Sales forecasting, model drift monitoring, "
        "alerting and guarded retraining evaluation."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "http://127.0.0.1:8501",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(predictions.router)
app.include_router(sales.router)
app.include_router(monitoring.router)
app.include_router(alerts.router)
app.include_router(models.router)
app.include_router(retraining.router)


@app.get("/")
def root():
    return {
        "name": "SalesGuard AI",
        "docs": "/docs",
        "health": "/health",
    }
