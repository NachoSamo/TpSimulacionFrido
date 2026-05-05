# Historial de Simulaciones — Guía de uso

## Levantar el sistema desde cero

```bash
# 1. Configurar variables de entorno
cp .env.example .env

# 2. Levantar PostgreSQL en Docker
docker-compose up -d

# 3. Instalar dependencias Python
cd backend
pip install -r requirements.txt

# 4. Aplicar migraciones (crea la tabla simulaciones)
alembic upgrade head

# 5. Levantar el backend
uvicorn main:app --port 8000
```

## Correr migraciones

```bash
# Desde backend/
alembic upgrade head      # aplicar todas las migraciones pendientes
alembic downgrade -1      # revertir la última migración
alembic current           # ver revisión actual
```

## Correr tests

```bash
# Desde backend/ (requiere solo Python, no Docker)
pytest
```

Los tests usan SQLite en memoria, por lo que no necesitan que Docker esté corriendo.

## Endpoints nuevos

### Listar todas las simulaciones

```bash
curl http://localhost:8000/api/simulaciones
```

Respuesta:
```json
[
  {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "creada_en": "2026-05-05T18:30:00Z",
    "n": 100000,
    "seed": 42,
    "estadisticas": {
      "tiempo_promedio_traslado": 30.78,
      "pct_detencion_y_parada_extra": 0.105,
      "cant_sin_detencion_ni_extra": 33106,
      "tiempo_maximo": 61.12,
      "tiempo_minimo": 10.03,
      "distribucion_lineas": { "2_etapas": {...}, "3_etapas": {...}, "4_etapas": {...} },
      "tiempo_promedio_por_linea": { "2_etapas": 25.1, "3_etapas": 30.4, "4_etapas": 35.2 },
      "pct_tiempo_perdido_detenciones": 0.129
    }
  }
]
```

### Detalle de una simulación

```bash
curl http://localhost:8000/api/simulaciones/3fa85f64-5717-4562-b3fc-2c963f66afa6
```

Respuesta: igual al listado pero incluye además el campo `config` con todos los parámetros usados.

Si el ID no existe: `404 Not Found`.
