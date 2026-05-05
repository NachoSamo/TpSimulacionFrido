from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session

from db.session import get_session
from services.historial_service import listar, obtener

router = APIRouter(prefix="/api/simulaciones", tags=["historial"])


# ---------- Schemas de respuesta ----------

class EstadisticasOut(BaseModel):
    tiempo_promedio_traslado: float
    pct_detencion_y_parada_extra: float
    cant_sin_detencion_ni_extra: int
    tiempo_maximo: float
    tiempo_minimo: float
    distribucion_lineas: Dict[str, Any]
    tiempo_promedio_por_linea: Dict[str, Any]
    pct_tiempo_perdido_detenciones: float


class SimulacionListItem(BaseModel):
    id: UUID
    creada_en: Any
    n: int
    seed: Optional[int]
    estadisticas: EstadisticasOut


class SimulacionDetalle(BaseModel):
    id: UUID
    creada_en: Any
    n: int
    seed: Optional[int]
    config: Dict[str, Any]
    estadisticas: EstadisticasOut


def _build_estadisticas(sim) -> EstadisticasOut:
    return EstadisticasOut(
        tiempo_promedio_traslado=sim.tiempo_promedio_traslado,
        pct_detencion_y_parada_extra=sim.pct_detencion_y_parada_extra,
        cant_sin_detencion_ni_extra=sim.cant_sin_detencion_ni_extra,
        tiempo_maximo=sim.tiempo_maximo,
        tiempo_minimo=sim.tiempo_minimo,
        distribucion_lineas=sim.distribucion_lineas,
        tiempo_promedio_por_linea=sim.tiempo_promedio_por_linea,
        pct_tiempo_perdido_detenciones=sim.pct_tiempo_perdido_detenciones,
    )


# ---------- Endpoints ----------

@router.get("", response_model=List[SimulacionListItem])
def listar_simulaciones(session: Session = Depends(get_session)):
    """Lista todas las simulaciones guardadas, más reciente primero."""
    sims = listar(session)
    return [
        SimulacionListItem(
            id=s.id,
            creada_en=s.creada_en,
            n=s.n,
            seed=s.seed,
            estadisticas=_build_estadisticas(s),
        )
        for s in sims
    ]


@router.get("/{id_simulacion}", response_model=SimulacionDetalle)
def obtener_simulacion(
    id_simulacion: UUID,
    session: Session = Depends(get_session),
):
    """Devuelve el detalle completo de una simulación, incluyendo config."""
    sim = obtener(session, id_simulacion)
    if sim is None:
        raise HTTPException(status_code=404, detail="Simulación no encontrada")

    return SimulacionDetalle(
        id=sim.id,
        creada_en=sim.creada_en,
        n=sim.n,
        seed=sim.seed,
        config=sim.config,
        estadisticas=_build_estadisticas(sim),
    )
