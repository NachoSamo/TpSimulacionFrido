from typing import Any, Dict
 
 
def calcular_estadisticas(fila_final: Dict[str, Any], n: int) -> Dict[str, Any]:
    """
    Calcula los 8 indicadores pedidos:
      1) Tiempo promedio de traslado
      2) % de ocasiones con detención + parada extra
      3) Cantidad de ciclos sin detención ni parada extra
      4) Tiempo máximo
      5) Tiempo mínimo
      6a) Distribución de uso de cada línea
      6b) Tiempo promedio por tipo de línea
      6c) % del tiempo total perdido en detenciones
    """
 
    # 1) Tiempo promedio (acumulador / N)
    tiempo_promedio = fila_final["acum_tiempo_total"] / n if n > 0 else 0.0
 
    # 2) % detención + parada extra
    pct_det_y_extra = (fila_final["acum_detencion_y_extra"] / n) if n > 0 else 0.0
 
    # 3) Cantidad sin detención ni extra
    cant_sin_nada = fila_final["acum_sin_detencion_ni_extra"]
 
    # 4) y 5) máx / mín
    tiempo_max = fila_final["max_historico"]
    tiempo_min = fila_final["min_historico"]
 
    # 6a) Distribución por línea
    c2 = fila_final["acum_count_2et"]
    c3 = fila_final["acum_count_3et"]
    c4 = fila_final["acum_count_4et"]
    total_lineas = c2 + c3 + c4 or 1   # evita división por cero
 
    distribucion_lineas = {
        "2_etapas": {"count": c2, "porcentaje": c2 / total_lineas},
        "3_etapas": {"count": c3, "porcentaje": c3 / total_lineas},
        "4_etapas": {"count": c4, "porcentaje": c4 / total_lineas},
    }
 
    # 6b) Tiempo promedio por tipo de línea
    promedio_por_linea = {
        "2_etapas": (fila_final["acum_tiempo_2et"] / c2) if c2 > 0 else 0.0,
        "3_etapas": (fila_final["acum_tiempo_3et"] / c3) if c3 > 0 else 0.0,
        "4_etapas": (fila_final["acum_tiempo_4et"] / c4) if c4 > 0 else 0.0,
    }
 
    # 6c) % tiempo perdido en detenciones (intermedia + extra)
    acum_total = fila_final["acum_tiempo_total"]
    pct_tiempo_perdido = (
        fila_final["acum_tiempo_perdido"] / acum_total if acum_total > 0 else 0.0
    )
 
    return {
        "tiempo_promedio_traslado": tiempo_promedio,
        "pct_detencion_y_parada_extra": pct_det_y_extra,
        "cant_sin_detencion_ni_extra": cant_sin_nada,
        "tiempo_maximo": tiempo_max,
        "tiempo_minimo": tiempo_min,
 
        # Las 3 variables extra (punto 6 del enunciado)
        "distribucion_lineas": distribucion_lineas,
        "tiempo_promedio_por_linea": promedio_por_linea,
        "pct_tiempo_perdido_detenciones": pct_tiempo_perdido,
    }