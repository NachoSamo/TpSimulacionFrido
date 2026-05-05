from typing import Any, Dict, List
 
import numpy as np
 
from models.config import SimConfig
from models.row_state import nueva_fila
from utils.generators import (
    crear_rng,
    rnd_bernoulli,
    rnd_discreta,
    rnd_normal,
    rnd_uniforme,
    rnd_uniform_01,
)
 
 
def _simular_ciclo(
    fila_actual: Dict[str, Any],
    fila_anterior: Dict[str, Any],
    cfg: SimConfig,
    rng: np.random.Generator,
    i: int,
) -> None:
    """
    Simula UN ciclo de producción. Pisa los valores de `fila_actual` in-place
    para evitar asignar memoria nueva en cada iteración.
 
    `fila_anterior` se usa solo para los acumuladores (sumar al valor previo).
    """
 
    # Reset de campos de la fila (los acumuladores se sobreescriben más abajo)
    for k in fila_actual:
        fila_actual[k] = 0
 
    fila_actual["i"] = i
 
    # ---------- 1) Elegir línea ----------
    rnd_l, cant_etapas = rnd_discreta(rng, cfg.lineas_etapas, cfg.lineas_prob)
    fila_actual["rnd_linea"] = rnd_l
    fila_actual["cant_etapas"] = cant_etapas
 
    # ---------- 2) Tiempos base de cada etapa (uniforme 5-8) ----------
    tiempos_base = [0.0, 0.0, 0.0, 0.0]
    for k in range(cant_etapas):
        rnd_t, t_base = rnd_uniforme(rng, cfg.etapa_tiempo_min, cfg.etapa_tiempo_max)
        fila_actual[f"rnd_t{k+1}"] = rnd_t
        fila_actual[f"t_base_{k+1}"] = t_base
        tiempos_base[k] = t_base
 
    # ---------- 3) Detención intermedia (60% de las veces) ----------
    rnd_det, hay_detencion = rnd_bernoulli(rng, cfg.p_detencion_intermedia)
    fila_actual["rnd_detencion"] = rnd_det
    fila_actual["hay_detencion"] = hay_detencion
 
    if hay_detencion:
        rnd_td, t_det = rnd_normal(rng, cfg.detencion_media_min, cfg.detencion_desv_min)
        fila_actual["rnd_t_detencion"] = rnd_td
        fila_actual["t_detencion"] = t_det
    # si no hay detención, queda en 0 (ya reseteado)
 
    # ---------- 4) Ajuste técnico (solo líneas de 2 y 3 etapas) ----------
    # Un solo RND decide si hay ajuste; un segundo RND elige qué etapa se ve afectada.
    aplica_ajuste = cant_etapas in (2, 3)
    hay_ajuste = False
    etapa_afectada = 0

    if aplica_ajuste:
        rnd_aj, hay_ajuste = rnd_bernoulli(rng, cfg.p_ajuste_tecnico)
        fila_actual["rnd_ajuste"] = rnd_aj
        fila_actual["hay_ajuste"] = hay_ajuste

        if hay_ajuste:
            rnd_sel, etapa_afectada = rnd_discreta(
                rng,
                list(range(1, cant_etapas + 1)),
                [1 / cant_etapas] * cant_etapas,
            )
            fila_actual["rnd_etapa_ajuste"] = rnd_sel
            fila_actual["etapa_ajustada"] = etapa_afectada
        else:
            fila_actual["rnd_etapa_ajuste"] = 0
            fila_actual["etapa_ajustada"] = 0
    else:
        fila_actual["rnd_ajuste"] = 0
        fila_actual["hay_ajuste"] = False
        fila_actual["rnd_etapa_ajuste"] = 0
        fila_actual["etapa_ajustada"] = 0

    suma_etapas = 0.0
    for k in range(cant_etapas):
        afectada = hay_ajuste and (k + 1 == etapa_afectada)
        fila_actual[f"ajuste_{k+1}"] = afectada
        t_etapa = tiempos_base[k] * (cfg.factor_ajuste if afectada else 1.0)
        fila_actual[f"t_etapa_{k+1}"] = t_etapa
        suma_etapas += t_etapa
 
    fila_actual["suma_etapas"] = suma_etapas
 
    # ---------- 5) Parada extra (70/400 = 17.5%) ----------
    rnd_pe, hay_extra = rnd_bernoulli(rng, cfg.p_parada_extra)
    fila_actual["rnd_parada_extra"] = rnd_pe
    fila_actual["hay_parada_extra"] = hay_extra
    fila_actual["t_parada_extra"] = cfg.parada_extra_min if hay_extra else 0.0
 
    # ---------- 6) Tiempo total del ciclo ----------
    tiempo_total = (
        fila_actual["suma_etapas"]
        + fila_actual["t_detencion"]
        + fila_actual["t_parada_extra"]
    )
    fila_actual["tiempo_total"] = tiempo_total
 
    # ---------- 7) Acumuladores ----------
    fila_actual["acum_tiempo_total"] = fila_anterior["acum_tiempo_total"] + tiempo_total
 
    # Punto 2 del enunciado: detuvo el recorrido Y hubo parada extra
    fila_actual["acum_detencion_y_extra"] = fila_anterior["acum_detencion_y_extra"] + (
        1 if (hay_detencion and hay_extra) else 0
    )
 
    # Punto 3 del enunciado: ni detención ni parada extra
    fila_actual["acum_sin_detencion_ni_extra"] = fila_anterior[
        "acum_sin_detencion_ni_extra"
    ] + (1 if (not hay_detencion and not hay_extra) else 0)
 
    # Máximo y mínimo histórico
    if i == 1:
        fila_actual["max_historico"] = tiempo_total
        fila_actual["min_historico"] = tiempo_total
    else:
        fila_actual["max_historico"] = max(fila_anterior["max_historico"], tiempo_total)
        fila_actual["min_historico"] = min(fila_anterior["min_historico"], tiempo_total)
 
    # Variables extra:
    # 1) Distribución de uso por línea
    fila_actual["acum_count_2et"] = fila_anterior["acum_count_2et"] + (1 if cant_etapas == 2 else 0)
    fila_actual["acum_count_3et"] = fila_anterior["acum_count_3et"] + (1 if cant_etapas == 3 else 0)
    fila_actual["acum_count_4et"] = fila_anterior["acum_count_4et"] + (1 if cant_etapas == 4 else 0)
 
    # 2) Tiempo acumulado por tipo de línea (para promedio al final)
    fila_actual["acum_tiempo_2et"] = fila_anterior["acum_tiempo_2et"] + (tiempo_total if cant_etapas == 2 else 0)
    fila_actual["acum_tiempo_3et"] = fila_anterior["acum_tiempo_3et"] + (tiempo_total if cant_etapas == 3 else 0)
    fila_actual["acum_tiempo_4et"] = fila_anterior["acum_tiempo_4et"] + (tiempo_total if cant_etapas == 4 else 0)
 
    # 3) Tiempo perdido en detenciones (intermedia + parada extra)
    tiempo_perdido_ciclo = fila_actual["t_detencion"] + fila_actual["t_parada_extra"]
    fila_actual["acum_tiempo_perdido"] = fila_anterior["acum_tiempo_perdido"] + tiempo_perdido_ciclo
 
 
def correr_simulacion(cfg: SimConfig) -> Dict[str, Any]:
    """
    Corre la simulación completa.
 
    Devuelve un dict con:
    - filas_visibles: lista de filas en el rango [fila_desde, fila_desde + cant_visibles - 1]
    - fila_final: la última fila simulada (i == N)
    - acumuladores_finales: la fila N (igual que fila_final, alias)
 
    Las estadísticas finales (los 8 puntos del enunciado) se calculan en
    stats_service a partir de fila_final.
    """
    cfg.validar()
 
    rng = crear_rng(cfg.seed)
 
    fila_a = nueva_fila()
    fila_b = nueva_fila()
 
    # Punteros (no copiamos en cada vuelta — solo intercambiamos referencias)
    fila_anterior = fila_a
    fila_actual = fila_b
 
    filas_visibles: List[Dict[str, Any]] = []
    fila_final: Dict[str, Any] = {}
 
    rango_inicio = cfg.fila_desde
    rango_fin = cfg.fila_desde + cfg.cant_visibles - 1
 
    for i in range(1, cfg.n + 1):
        _simular_ciclo(fila_actual, fila_anterior, cfg, rng, i)
 
        # Guardar copia si está en el rango visible
        if rango_inicio <= i <= rango_fin:
            filas_visibles.append(dict(fila_actual))
 
        # Guardar copia de la última fila
        if i == cfg.n:
            fila_final = dict(fila_actual)
 
        # Rotar punteros: la actual pasa a ser anterior en la próxima iteración.
        fila_anterior, fila_actual = fila_actual, fila_anterior
 
    return {
        "filas_visibles": filas_visibles,
        "fila_final": fila_final,
        "rango_visible": {"desde": rango_inicio, "hasta": min(rango_fin, cfg.n)},
        "n": cfg.n,
    }