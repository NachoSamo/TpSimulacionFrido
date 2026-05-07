import logging
from typing import Generator

from sqlalchemy import text
from sqlmodel import Session, create_engine

from db.settings import settings

logger = logging.getLogger(__name__)

engine = None

#Validamos que la base de datos este disponible
def init_engine() -> None:
    global engine
    try:
        _engine = create_engine(
            settings.DATABASE_URL,
            echo=False,
            connect_args={"connect_timeout": 5},
        )
        with _engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        engine = _engine
        logger.info("Base de datos conectada correctamente en %s", settings.DATABASE_URL)
    except Exception as exc:
        logger.error(
            "La base de datos no está disponible. Verificá que Docker/PostgreSQL "
            "esté corriendo. Detalle: %s",
            exc,
        )


def get_session() -> Generator[Session, None, None]:
    if engine is None:
        raise RuntimeError(
            "La base de datos no está disponible. "
            "Iniciá el contenedor PostgreSQL antes de usar este endpoint."
        )
    with Session(engine) as session:
        yield session
