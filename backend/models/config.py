from dataclasses import dataclass, field
from typing import List, Tuple
 
 
@dataclass
class SimConfig:
    # ---------- Parámetros de corrida ----------
    n: int = 100_000              # cantidad total de ciclos a simular
    fila_desde: int = 1           # primera fila visible (1-indexed)
    cant_visibles: int = 200      # cantidad de filas a mostrar a partir de fila_desde
    seed: int | None = None       # semilla opcional para reproducibilidad
 
    # ---------- Líneas de procesamiento ----------
    # Probabilidades de cada línea (deben sumar 1.0).
    # El orden corresponde a las cantidades de etapas en `lineas_etapas`.
    lineas_prob: Tuple[float, float, float] = (0.30, 0.45, 0.25)
    lineas_etapas: Tuple[int, int, int] = (2, 3, 4)
 
    # ---------- Detención intermedia ----------
    p_detencion_intermedia: float = 0.60
    detencion_media_seg: float = 240.0     # 4 minutos
    detencion_desv_seg: float = 35.0       # ±35 segundos = σ (interpretación literal)
 
    # ---------- Ajuste técnico (solo líneas 2 y 3 etapas) ----------
    p_ajuste_tecnico: float = 0.60
    factor_ajuste: float = 2.0             # se duplica el tiempo
 
    # ---------- Tiempo base por etapa ----------
    etapa_tiempo_min: float = 5.0          # uniforme [5, 8]
    etapa_tiempo_max: float = 8.0
 
    # ---------- Parada extra ----------
    # 70 de cada 400 ciclos -> 0.175
    p_parada_extra: float = 70.0 / 400.0
    parada_extra_min: float = 9.0          # 9 minutos fijos
 
    # ---------- Conversiones derivadas (en minutos) ----------
    @property
    def detencion_media_min(self) -> float:
        return self.detencion_media_seg / 60.0
 
    @property
    def detencion_desv_min(self) -> float:
        return self.detencion_desv_seg / 60.0
 
    # ---------- Validación de la configuración de la simulacion que ingresa el usuario
    def validar(self) -> None:
        if self.n < 1:
            raise ValueError("n debe ser >= 1")
        if not (1 <= self.fila_desde <= self.n):
            raise ValueError("fila_desde fuera de rango")
        if self.cant_visibles < 1:
            raise ValueError("cant_visibles debe ser >= 1")
        if abs(sum(self.lineas_prob) - 1.0) > 1e-6:
            raise ValueError(
                f"Las probabilidades de líneas deben sumar 1.0 "
                f"(suma actual: {sum(self.lineas_prob)})"
            )
        if len(self.lineas_prob) != len(self.lineas_etapas):
            raise ValueError("lineas_prob y lineas_etapas deben tener la misma longitud")
        for p, nombre in [
            (self.p_detencion_intermedia, "p_detencion_intermedia"),
            (self.p_ajuste_tecnico, "p_ajuste_tecnico"),
            (self.p_parada_extra, "p_parada_extra"),
        ]:
            if not (0.0 <= p <= 1.0):
                raise ValueError(f"{nombre} debe estar en [0, 1]")
        if self.etapa_tiempo_min >= self.etapa_tiempo_max:
            raise ValueError("etapa_tiempo_min debe ser < etapa_tiempo_max")
 