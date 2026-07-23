"""
app/services/rating_shim.py — Rating shim for elo/poisson models.

This module MUST be importable at joblib unpickling time.
Do not move or rename without regenerating elo_v1.pkl and poisson_v1.pkl.
"""
import numpy as np
from sklearn.linear_model import Ridge


class RatingShim:
    """
    Wraps a Ridge regressor in a classifier-compatible interface.
    Used for ELO rating and Poisson regression models.
    predict_proba returns a 2-column array [P(no), P(yes)].
    """

    def __init__(self):
        self.model = Ridge()

    def fit(self, X, y):
        self.model.fit(X, y)
        return self

    def predict_proba(self, X):
        p = np.clip(self.model.predict(X), 0, 1).reshape(-1, 1)
        return np.hstack([1 - p, p])

    def predict(self, X):
        return (self.model.predict(X) > 0.5).astype(int)
