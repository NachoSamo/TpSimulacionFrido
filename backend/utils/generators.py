from typing import Sequence, Tuple
import numpy as np
 
 
def rnd_uniform_01(rng: np.random.Generator) -> float:
    """RND uniforme en [0, 1). Es el 'tirar el dado' base de Montecarlo."""
    return float(rng.random())
 
 
def rnd_uniforme(rng: np.random.Generator, low: float, high: float) -> Tuple[float, float]:
    """
    Devuelve (rnd, valor) donde:
    - rnd: número uniforme en [0, 1)
    - valor: tiempo en [low, high) usando ese rnd
 
    Esto se usa para el tiempo base de cada etapa (5–8 min) y permite
    mostrar el RND original como columna en el reporte.
    """
    rnd = rnd_uniform_01(rng)
    valor = low + rnd * (high - low)
    return rnd, valor
 
 
def rnd_normal(rng: np.random.Generator, media: float, desv: float) -> Tuple[float, float]:
    """
    Devuelve (rnd, valor) para una distribución normal.
 
    Importante: para una normal no se puede generar 'a partir de un único RND
    uniforme' de forma directa (la inversa de la normal no es analítica).
    Usamos `rng.normal()` directamente y devolvemos un rnd uniforme aparte
    SOLO para mostrarlo en la tabla, igual que hace el Excel adjunto.
 
    El truncado en 0 evita tiempos negativos (la cola izquierda de la normal
    podría dar valores < 0 con σ alto, aunque acá es muy improbable).
    """
    rnd = rnd_uniform_01(rng)
    valor = float(rng.normal(loc=media, scale=desv))
    if valor < 0:
        valor = 0.0
    return rnd, valor
 
 
def rnd_discreta(
    rng: np.random.Generator,
    valores: Sequence[int],
    probabilidades: Sequence[float],
) -> Tuple[float, int]:
    """
    Elige un valor discreto según probabilidades acumuladas.
 
    Ej: valores=(2,3,4), probabilidades=(0.30, 0.45, 0.25)
        -> rnd 0.00–0.29 -> 2 etapas
        -> rnd 0.30–0.74 -> 3 etapas
        -> rnd 0.75–0.99 -> 4 etapas
 
    Devuelve (rnd, valor_elegido).
    """
    rnd = rnd_uniform_01(rng)
    acum = 0.0
    for valor, prob in zip(valores, probabilidades):
        acum += prob
        if rnd < acum:
            return rnd, valor
    # Fallback por errores de redondeo de punto flotante (rnd ≈ 1.0)
    return rnd, valores[-1]
 
 
def rnd_bernoulli(rng: np.random.Generator, p: float) -> Tuple[float, bool]:
    """
    Tira una moneda con probabilidad p de salir True.
 
    Convención del enunciado / Excel:
    - rnd < p  -> ocurre el evento (True)
    - rnd >= p -> no ocurre (False)
 
    Se usa para: detención intermedia, ajuste técnico por etapa, parada extra.
    """
    rnd = rnd_uniform_01(rng)
    return rnd, rnd < p
 
 
def crear_rng(seed: int | None = None) -> np.random.Generator:
    """Fábrica del generador. Si seed es None -> aleatoria del sistema."""
    return np.random.default_rng(seed)