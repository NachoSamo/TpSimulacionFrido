from datetime import datetime, timezone
from typing import Any, Optional
from uuid import UUID, uuid4

import sqlalchemy as sa
from sqlmodel import Field, SQLModel


class Simulacion(SQLModel, table=True):
    __tablename__ = "simulaciones"

    __table_args__ = (
        sa.Index("idx_simulaciones_creada_en", "creada_en"),
    )

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    creada_en: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    n: int
    seed: Optional[int] = Field(default=None)

    # Columnas JSONB en PostgreSQL; sa.JSON es compatible con SQLite para tests
    config: Optional[Any] = Field(
        default=None,
        sa_column=sa.Column("config", sa.JSON, nullable=False),
    )

    tiempo_promedio_traslado: float
    pct_detencion_y_parada_extra: float
    cant_sin_detencion_ni_extra: int
    tiempo_maximo: float
    tiempo_minimo: float

    distribucion_lineas: Optional[Any] = Field(
        default=None,
        sa_column=sa.Column("distribucion_lineas", sa.JSON, nullable=False),
    )
    tiempo_promedio_por_linea: Optional[Any] = Field(
        default=None,
        sa_column=sa.Column("tiempo_promedio_por_linea", sa.JSON, nullable=False),
    )

    pct_tiempo_perdido_detenciones: float
