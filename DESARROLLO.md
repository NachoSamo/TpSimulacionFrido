# Guía de desarrollo — FRIDO (Windows)

## Requisitos previos

| Herramienta | Versión mínima | Verificar con |
|---|---|---|
| Python | 3.12+ | `python --version` |
| Node.js | 18+ | `node --version` |
| Docker Desktop | cualquiera | `docker --version` |
| Git | cualquiera | `git --version` |

---

## 1. Base de datos (PostgreSQL en Docker)

### Primera vez

```powershell
# Desde la raíz del repo
cp .env.example .env
docker-compose up -d
```

### Verificar que está corriendo

```powershell
docker-compose ps
# El servicio "postgres" debe tener estado "healthy"
```

### Comandos útiles

```powershell
docker-compose stop       # detener sin borrar datos
docker-compose start      # volver a levantar
docker-compose down       # detener y remover contenedor (los datos persisten en el volumen)
docker-compose down -v    # detener Y borrar todos los datos (destructivo)
```

---

## 2. Backend (FastAPI + Python)

### Primera vez: crear entorno virtual e instalar dependencias

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

> Si PowerShell bloquea la ejecución del `.ps1`, ejecutá esto una vez:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

### Correr migraciones (crear tablas en la DB)

```powershell
# Con el venv activado, desde backend/
alembic upgrade head
```

### Levantar el servidor

```powershell
# Con el venv activado, desde backend/
uvicorn main:app --reload --port 8000
```

El backend queda disponible en `http://localhost:8000`.  
Documentación interactiva: `http://localhost:8000/docs`

### Sesiones siguientes (venv ya creado)

```powershell
cd backend
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload --port 8000
```

### Correr tests

```powershell
# Con el venv activado, desde backend/
# No requiere Docker — usa SQLite en memoria
pytest
```

---

## 3. Frontend (React + Vite)

### Primera vez: instalar dependencias

```powershell
cd frontend
npm install
```

### Levantar el servidor de desarrollo

```powershell
# Desde frontend/
npm run dev
```

El frontend queda disponible en `http://localhost:5173`.

### Sesiones siguientes

```powershell
cd frontend
npm run dev
```

---

## 4. Orden de arranque recomendado

Abrir **tres terminales de PowerShell** independientes:

**Terminal 1 — Base de datos**
```powershell
cd C:\Users\Nacho\TpSimulacionFrido
docker-compose up
```

**Terminal 2 — Backend**
```powershell
cd C:\Users\Nacho\TpSimulacionFrido\backend
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload --port 8000
```

**Terminal 3 — Frontend**
```powershell
cd C:\Users\Nacho\TpSimulacionFrido\frontend
npm run dev
```

---

## 5. Puertos utilizados

| Servicio | Puerto | URL |
|---|---|---|
| Frontend (Vite) | 5173 | http://localhost:5173 |
| Backend (FastAPI) | 8000 | http://localhost:8000 |
| PostgreSQL | 5432 | — (interno) |
| API docs (Swagger) | 8000 | http://localhost:8000/docs |

---

## 6. Solución de problemas frecuentes

**`uvicorn` no se reconoce**  
El venv no está activado. Ejecutá `.\venv\Scripts\Activate.ps1` primero,  
o usá la ruta completa: `.\venv\Scripts\uvicorn.exe main:app --reload --port 8000`

**Error de política de ejecución de scripts**  
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**`alembic upgrade head` falla con "connection refused"**  
Docker no está corriendo o la DB no terminó de iniciar. Verificá con `docker-compose ps` que el estado sea `healthy`.

**Error "module not found" al correr el backend**  
Asegurate de estar dentro de `backend/` con el venv activado antes de correr `uvicorn`.

**Puerto 5432 ya en uso**  
Tenés otro PostgreSQL corriendo localmente. Cambiá `POSTGRES_PORT` en `.env` (ej: `5433`) y actualizá también `DATABASE_URL`.
