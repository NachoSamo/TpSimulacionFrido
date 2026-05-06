"""Crea tabla simulaciones con índice sobre creada_en

Revision ID: 0001
Revises:
Create Date: 2026-05-05

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB, UUID

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "simulaciones",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            primary_key=True,
            nullable=False,
        ),
        sa.Column("creada_en",
        sa.TIMESTAMP(timezone=True),
        server_default=sa.text("now()"),
        nullable=False,
    ),
        sa.Column("n", sa.Integer(), nullable=False),
        sa.Column("seed", sa.BigInteger(), nullable=True),
        sa.Column("config", JSONB(), nullable=False),
        sa.Column("tiempo_promedio_traslado", sa.Float(), nullable=False),
        sa.Column("pct_detencion_y_parada_extra", sa.Float(), nullable=False),
        sa.Column("cant_sin_detencion_ni_extra", sa.Integer(), nullable=False),
        sa.Column("tiempo_maximo", sa.Float(), nullable=False),
        sa.Column("tiempo_minimo", sa.Float(), nullable=False),
        sa.Column("distribucion_lineas", JSONB(), nullable=False),
        sa.Column("tiempo_promedio_por_linea", JSONB(), nullable=False),
        sa.Column("pct_tiempo_perdido_detenciones", sa.Float(), nullable=False),
    )
    op.create_index(
        "idx_simulaciones_creada_en",
        "simulaciones",
        [sa.text("creada_en DESC")],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("idx_simulaciones_creada_en", table_name="simulaciones")
    op.drop_table("simulaciones")
