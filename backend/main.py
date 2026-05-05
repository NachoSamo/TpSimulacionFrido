from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
 
from controllers.simulation_controller import router as simulacion_router
 
 
app = FastAPI(
    title="FRIDO - Simulación Montecarlo",
    description="Simulación del proceso de fabricación de helados",
    version="0.1.0",
)
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
app.include_router(simulacion_router)
 
 
@app.get("/")
def health_check() -> dict:
    return {"status": "ok", "service": "frido-backend"}