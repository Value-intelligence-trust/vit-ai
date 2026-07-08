import math
from typing import Tuple, List, Dict

def normalise(*args) -> Tuple[float, ...]:
    s = sum(args)
    return tuple(p / s for p in args) if s > 0 else tuple(1.0/len(args) for _ in args)

def vig_free(h: float, d: float, a: float) -> Tuple[float, float, float]:
    return normalise(1/h, 1/d, 1/a)

def market_to_xg(hp: float, ap: float, dp: float) -> Tuple[float, float]:
    total_xg = 2.5 + (dp - 0.25) * 4.0
    h_ratio = hp / (hp + ap)
    return max(0.1, total_xg * h_ratio), max(0.1, total_xg * (1 - h_ratio))

def poisson_pmf(k: int, lam: float) -> float:
    if lam <= 0: return 1.0 if k == 0 else 0.0
    return (lam**k * math.exp(-lam)) / math.factorial(k)

def confidence_from_probs(hp: float, dp: float, ap: float) -> float:
    probs = [p for p in (hp, dp, ap) if p > 0]
    ent = -sum(p * math.log(p) for p in probs) if probs else math.log(3)
    return round(1.0 - ent/math.log(3), 3)

def build_score_matrix(lam_h: float, lam_a: float, max_g: int = 6) -> List[List[float]]:
    return [[poisson_pmf(h, lam_h) * poisson_pmf(a, lam_a) for a in range(max_g+1)] for h in range(max_g+1)]
