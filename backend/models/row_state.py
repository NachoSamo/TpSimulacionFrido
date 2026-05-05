from typing import Any, Dict
 
ROW_KEYS = [
    "i",
 
    # Línea elegida
    "rnd_linea",
    "cant_etapas",                  # 2, 3 o 4
 
    # Tiempos base por etapa (uniforme 5-8). NaN si la etapa no existe.
    "rnd_t1", "t_base_1",
    "rnd_t2", "t_base_2",
    "rnd_t3", "t_base_3",
    "rnd_t4", "t_base_4",
 
    # Detención intermedia
    "rnd_detencion",
    "hay_detencion",                # bool
    "rnd_t_detencion",              # solo si hay_detencion
    "t_detencion",                  # tiempo en min, 0 si no hay
 
    # Ajuste técnico (solo 2 y 3 etapas)
    "rnd_ajuste",        # RND que determinó si hay ajuste en la línea
    "hay_ajuste",        # bool
    "rnd_etapa_ajuste",  # RND que seleccionó la etapa afectada
    "etapa_ajustada",    # 1, 2 o 3 (la etapa afectada); 0 si no hay ajuste
    "ajuste_1", "t_etapa_1",
    "ajuste_2", "t_etapa_2",
    "ajuste_3", "t_etapa_3",
 
    # Suma de etapas con ajuste aplicado (no incluye detención ni parada extra)
    "suma_etapas",
 
    # Parada extra
    "rnd_parada_extra",
    "hay_parada_extra",             # bool
    "t_parada_extra",               # 9 o 0
 
    # Total del ciclo
    "tiempo_total",
 
    # Acumuladores (la consigna pide que los acumuladores estén como columnas)
    "acum_tiempo_total",
    "acum_detencion_y_extra",       # cant. ciclos con detención intermedia Y parada extra
    "acum_sin_detencion_ni_extra",  # cant. ciclos sin ninguna de las dos
    "max_historico",
    "min_historico",
 
    # ---- Acumuladores para las 3 variables extra ----
    # 1) Distribución de uso de cada línea
    "acum_count_2et", "acum_count_3et", "acum_count_4et",
    # 2) Tiempo promedio por tipo de línea (acumulamos suma; el promedio se calcula al final)
    "acum_tiempo_2et", "acum_tiempo_3et", "acum_tiempo_4et",
    # 3) % tiempo perdido en detenciones (acumulamos suma de tiempos de detención + extras)
    "acum_tiempo_perdido",          # suma de t_detencion + t_parada_extra
]
 
 
def nueva_fila() -> Dict[str, Any]:
    """Crea una fila inicializada en 0 / None."""
    return {k: 0 for k in ROW_KEYS}