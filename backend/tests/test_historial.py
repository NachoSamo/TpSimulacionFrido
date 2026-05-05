"""
Tests del historial de simulaciones.
Cubre: CA-2, CA-4, CA-5, CA-6, CA-7, CA-8, CA-10.
"""
from uuid import UUID, uuid4

import pytest

from models.config import SimConfig

STATS_FAKE = {
    "tiempo_promedio_traslado": 30.5,
    "pct_detencion_y_parada_extra": 0.1,
    "cant_sin_detencion_ni_extra": 1000,
    "tiempo_maximo": 60.0,
    "tiempo_minimo": 10.0,
    "distribucion_lineas": {
        "2_etapas": {"count": 300, "porcentaje": 0.30},
        "3_etapas": {"count": 450, "porcentaje": 0.45},
        "4_etapas": {"count": 250, "porcentaje": 0.25},
    },
    "tiempo_promedio_por_linea": {
        "2_etapas": 25.0,
        "3_etapas": 30.0,
        "4_etapas": 35.0,
    },
    "pct_tiempo_perdido_detenciones": 0.12,
}


# ---------- Tests del service ----------

class TestHistorialService:
    def test_persistir_retorna_uuid(self, session):
        from services.historial_service import persistir

        cfg = SimConfig(n=1000, seed=42)
        id_sim = persistir(session, cfg, STATS_FAKE, 1000)
        assert isinstance(id_sim, UUID)

    def test_persistir_guarda_datos_correctos(self, session):
        from services.historial_service import obtener, persistir

        cfg = SimConfig(n=500, seed=7)
        id_sim = persistir(session, cfg, STATS_FAKE, 500)

        sim = obtener(session, id_sim)
        assert sim is not None
        assert sim.n == 500
        assert sim.seed == 7
        assert sim.tiempo_promedio_traslado == 30.5
        assert sim.cant_sin_detencion_ni_extra == 1000

    def test_listar_vacio(self, session):
        from services.historial_service import listar

        result = listar(session)
        assert result == []

    def test_listar_retorna_todos(self, session):
        from services.historial_service import listar, persistir

        cfg = SimConfig(n=100)
        persistir(session, cfg, STATS_FAKE, 100)
        persistir(session, cfg, STATS_FAKE, 200)
        persistir(session, cfg, STATS_FAKE, 300)

        result = listar(session)
        assert len(result) == 3

    def test_obtener_existente(self, session):
        from services.historial_service import obtener, persistir

        cfg = SimConfig(n=100)
        id_sim = persistir(session, cfg, STATS_FAKE, 100)
        sim = obtener(session, id_sim)
        assert sim is not None
        assert sim.id == id_sim

    def test_obtener_no_existente_retorna_none(self, session):
        from services.historial_service import obtener

        result = obtener(session, uuid4())
        assert result is None


# ---------- Tests de endpoints ----------

class TestEndpointListado:
    def test_listado_vacio_devuelve_array_vacio(self, client):
        """CA-4: listado vacío retorna [] con status 200."""
        resp = client.get("/api/simulaciones")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_listado_con_datos(self, client):
        """CA-5: tras varias corridas, el listado las devuelve todas."""
        for n in [100, 200, 300]:
            client.post("/api/simulacion/run", json={"n": n})

        resp = client.get("/api/simulaciones")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 3

    def test_listado_no_incluye_config(self, client):
        """El listado devuelve estadísticas pero NO config (es para el detalle)."""
        client.post("/api/simulacion/run", json={"n": 100})

        resp = client.get("/api/simulaciones")
        item = resp.json()[0]
        assert "estadisticas" in item
        assert "config" not in item

    def test_listado_tiene_campos_requeridos(self, client):
        client.post("/api/simulacion/run", json={"n": 100})

        item = client.get("/api/simulaciones").json()[0]
        for campo in ("id", "creada_en", "n", "estadisticas"):
            assert campo in item


class TestEndpointDetalle:
    def test_detalle_existente(self, client):
        """CA-6: GET /{id} devuelve config y estadísticas."""
        run_resp = client.post("/api/simulacion/run", json={"n": 100, "seed": 7})
        id_sim = run_resp.json()["id_simulacion"]

        resp = client.get(f"/api/simulaciones/{id_sim}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == id_sim
        assert "config" in data
        assert "estadisticas" in data

    def test_detalle_no_existente_devuelve_404(self, client):
        """CA-7: UUID válido pero inexistente → 404."""
        resp = client.get(f"/api/simulaciones/{uuid4()}")
        assert resp.status_code == 404

    def test_detalle_uuid_invalido(self, client):
        """CA-8: UUID inválido → 404 o 422."""
        resp = client.get("/api/simulaciones/no-es-un-uuid")
        assert resp.status_code in (404, 422)


class TestEndpointRun:
    def test_run_incluye_id_simulacion(self, client):
        """CA-2: la response de /run incluye id_simulacion con formato UUID válido."""
        resp = client.post("/api/simulacion/run", json={"n": 100, "seed": 42})
        assert resp.status_code == 200
        data = resp.json()
        assert "id_simulacion" in data
        UUID(data["id_simulacion"])  # lanza ValueError si no es UUID válido

    def test_run_persiste_en_bd(self, client):
        """CA-2: tras el run, el id retornado existe en el listado."""
        resp = client.post("/api/simulacion/run", json={"n": 100, "seed": 42})
        id_sim = resp.json()["id_simulacion"]

        detalle = client.get(f"/api/simulaciones/{id_sim}")
        assert detalle.status_code == 200

    def test_run_mantiene_campos_existentes(self, client):
        """CA-10: la response sigue teniendo todos los campos anteriores."""
        resp = client.post("/api/simulacion/run", json={"n": 100})
        assert resp.status_code == 200
        data = resp.json()
        for campo in ("n", "rango_visible", "filas_visibles", "fila_final", "estadisticas"):
            assert campo in data, f"Campo '{campo}' falta en la response"

    def test_run_config_default_no_cambia(self, client):
        """CA-10: GET /config-default sigue funcionando."""
        resp = client.get("/api/simulacion/config-default")
        assert resp.status_code == 200
        data = resp.json()
        assert "n" in data
        assert "lineas_prob" in data

    def test_health_check_no_cambia(self, client):
        """CA-10: GET / sigue devolviendo el health check."""
        resp = client.get("/")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"
