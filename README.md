# FRIDO - Simulación de Montecarlo (TP3)

Este proyecto desarrolla una solución de software para simular el proceso de fabricación de helados de la planta **FRIDO**, utilizando el método de **Montecarlo**. La aplicación permite analizar la eficiencia productiva basándose en decisiones probabilísticas, tiempos variables y paradas técnicas[cite: 24].

## 🚀 Tecnologías Utilizadas

* **Frontend:** React + TypeScript + Tailwind CSS (Vite).
* **Backend:** Python con FastAPI.
* **Lógica de Simulación:** Algoritmo de Montecarlo con gestión de memoria optimizada (2 filas).

## 📋 Descripción del Problema

La producción de helados en FRIDO atraviesa diversas etapas con las siguientes variables:
* **Líneas de Proceso:** 3 opciones (2, 3 o 4 etapas) con probabilidades de 30%, 45% y 25%.
* **Paradas de Control:** 60% de probabilidad, sumando un tiempo con distribución Normal ($\mu=4min, \sigma=35seg$).
* **Ajustes Técnicos:** En líneas de 2 y 3 etapas (60% de probabilidad), el tiempo de la etapa se duplica.
* **Tiempos de Etapa:** Distribución Uniforme entre 5 y 8 minutos.
* **Paradas Administrativas:** Demora fija de 9 minutos en 70 de cada 400 ciclos.

## 📊 Objetivos de la Simulación

El sistema permite calcular y visualizar:
1.  Tiempo promedio de traslado total.
2.  Porcentaje de ocasiones con paradas en etapa y paradas extras simultáneas.
3.  Contador de ciclos sin interrupciones ni paradas extras.
4.  Tiempos máximos y mínimos de fabricación registrados.
5.  Análisis de 3 variables adicionales propuestas por el equipo.

## 🛠️ Características del Software

* **Configuración Dinámica:** Soporta el ingreso de parámetros (probabilidades, variables de distribución, etc.) antes de iniciar la corrida.
* **Gestión de Memoria:** El motor de simulación trabaja exclusivamente con **2 filas en memoria** para optimizar el rendimiento.
* **Visualización de Resultados:**
    * Muestra un vector de estado desde la fila $i$ hasta $i+200$.
    * Visualización obligatoria de la **última fila simulada (N)**.
    * Interfaz moderna con Tailwind CSS, evitando salidas por consola.

## 🏗️ Estructura del Proyecto

```text
├── backend/
│   ├── main.py            # Endpoints de FastAPI
│   ├── simulation_engine.py # Lógica de Montecarlo y distribuciones
│   └── models.py          # Esquemas de datos (Pydantic)
├── frontend/
│   ├── src/
│   │   ├── components/    # Tablas de resultados y formularios de carga
│   │   ├── hooks/         # Lógica de llamadas a la API
│   │   └── App.tsx
└── README.md
```

## ⚙️ Instalación y Ejecución

1.  **Backend (Python):**
    ```bash
    cd backend
    pip install fastapi uvicorn
    uvicorn main:app --reload
    ```
2.  **Frontend (React):**
    ```bash
    cd frontend
    npm install
    npm run dev
    ```