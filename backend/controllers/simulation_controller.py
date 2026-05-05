import logging
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlmodel import Session

from db.session import get_session
from models.config import SimConfig
from services.historial_service import persistir
from services.simulation_service import correr_simulacion
from services.stats_service import calcular_estadisticas

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/simulacion", tags=["simulacion"])


# ---------- Schemas Pydantic ----------

class SimConfigRequest(BaseModel):
    """Body del POST. Todos los campos son opcionales — usan los defaults
    del SimConfig si no se envían."""

    n: int = Field(100_000, ge=1, le=1_000_000)
    fila_desde: int = Field(1, ge=1)
    cant_visibles: int = Field(200, ge=1, le=1000)
    seed: Optional[int] = None

    lineas_prob: Optional[Tuple[float, float, float]] = None
    lineas_etapas: Optional[Tuple[int, int, int]] = None

    p_detencion_intermedia: Optional[float] = Field(None, ge=0, le=1)
    detencion_media_seg: Optional[float] = None
    detencion_desv_seg: Optional[float] = None

    p_ajuste_tecnico: Optional[float] = Field(None, ge=0, le=1)
    factor_ajuste: Optional[float] = None

    etapa_tiempo_min: Optional[float] = None
    etapa_tiempo_max: Optional[float] = None

    p_parada_extra: Optional[float] = Field(None, ge=0, le=1)
    parada_extra_min: Optional[float] = None

    def to_sim_config(self) -> SimConfig:
        """Construye un SimConfig usando solo los valores no-None."""
        valores = {k: v for k, v in self.model_dump().items() if v is not None}
        return SimConfig(**valores)


class SimulacionResponse(BaseModel):
    id_simulacion: UUID
    n: int
    rango_visible: Dict[str, int]
    filas_visibles: List[Dict[str, Any]]
    fila_final: Dict[str, Any]
    estadisticas: Dict[str, Any]


# ---------- Endpoints ----------

@router.post("/run", response_model=SimulacionResponse)
def ejecutar_simulacion(
    req: SimConfigRequest,
    session: Session = Depends(get_session),
) -> SimulacionResponse:
    """Corre la simulación con la config recibida y persiste el resultado."""
    try:
        cfg = req.to_sim_config()
        resultado = correr_simulacion(cfg)
        stats = calcular_estadisticas(resultado["fila_final"], cfg.n)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        id_sim = persistir(session, cfg, stats, resultado["n"])
    except Exception:
        logger.exception("Error al persistir la simulación en la base de datos")
        raise HTTPException(
            status_code=500,
            detail="Error al guardar la simulación en la base de datos",
        )

    return SimulacionResponse(
        id_simulacion=id_sim,
        n=resultado["n"],
        rango_visible=resultado["rango_visible"],
        filas_visibles=resultado["filas_visibles"],
        fila_final=resultado["fila_final"],
        estadisticas=stats,
    )


@router.get("/config-default")
def obtener_config_default() -> Dict[str, Any]:
    """Devuelve la configuración por defecto (útil para que el frontend
    pre-rellene el formulario)."""
    cfg = SimConfig()
    return {
        "n": cfg.n,
        "fila_desde": cfg.fila_desde,
        "cant_visibles": cfg.cant_visibles,
        "lineas_prob": list(cfg.lineas_prob),
        "lineas_etapas": list(cfg.lineas_etapas),
        "p_detencion_intermedia": cfg.p_detencion_intermedia,
        "detencion_media_seg": cfg.detencion_media_seg,
        "detencion_desv_seg": cfg.detencion_desv_seg,
        "p_ajuste_tecnico": cfg.p_ajuste_tecnico,
        "factor_ajuste": cfg.factor_ajuste,
        "etapa_tiempo_min": cfg.etapa_tiempo_min,
        "etapa_tiempo_max": cfg.etapa_tiempo_max,
        "p_parada_extra": cfg.p_parada_extra,
        "parada_extra_min": cfg.parada_extra_min,
    }
