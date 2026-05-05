import dataclasses
from uuid import UUID

from sqlmodel import Session, select

from models.config import SimConfig
from models.simulacion_db import Simulacion


def persistir(session: Session, cfg: SimConfig, stats: dict, n: int) -> UUID:
    """Persiste una simulación y retorna su UUID."""
    config_dict = dataclasses.asdict(cfg)
    # Convertir tuplas a listas para serialización JSON limpia
    config_dict["lineas_prob"] = list(config_dict["lineas_prob"])
    config_dict["lineas_etapas"] = list(config_dict["lineas_etapas"])

    sim = Simulacion(
        n=n,
        seed=cfg.seed,
        config=config_dict,
        tiempo_promedio_traslado=stats["tiempo_promedio_traslado"],
        pct_detencion_y_parada_extra=stats["pct_detencion_y_parada_extra"],
        cant_sin_detencion_ni_extra=stats["cant_sin_detencion_ni_extra"],
        tiempo_maximo=stats["tiempo_maximo"],
        tiempo_minimo=stats["tiempo_minimo"],
        distribucion_lineas=stats["distribucion_lineas"],
        tiempo_promedio_por_linea=stats["tiempo_promedio_por_linea"],
        pct_tiempo_perdido_detenciones=stats["pct_tiempo_perdido_detenciones"],
    )

    session.add(sim)
    session.commit()
    session.refresh(sim)
    return sim.id


def listar(session: Session) -> list[Simulacion]:
    """Lista todas las simulaciones ordenadas por fecha de creación descendente."""
    statement = select(Simulacion).order_by(Simulacion.creada_en.desc())
    return list(session.exec(statement).all())


def obtener(session: Session, id_simulacion: UUID) -> Simulacion | None:
    """Retorna la simulación con el ID dado, o None si no existe."""
    return session.get(Simulacion, id_simulacion)
