import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controllers.historial_controller import router as historial_router
from controllers.simulation_controller import router as simulacion_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    from db.session import init_engine
    init_engine()
    yield


app = FastAPI(
    title="FRIDO - Simulación Montecarlo",
    description="Simulación del proceso de fabricación de helados",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(simulacion_router)
app.include_router(historial_router)


@app.get("/")
def health_check() -> dict:
    return {"status": "ok", "service": "frido-backend"}
