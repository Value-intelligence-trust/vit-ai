#!/usr/bin/env python3
"""Seed VIT AI model artifacts — runs at Docker build time.

Generates and saves all 16 VIT ensemble model artifacts as .pkl files.
RatingShim is imported from app.services.rating_shim so it is always
deserializable when joblib loads the pickled files at runtime.
"""
import os
import sys
import joblib
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier

# RatingShim must be imported from its canonical module so joblib can
# deserialize elo_v1.pkl and poisson_v1.pkl at runtime.
from app.services.rating_shim import RatingShim

try:
    from xgboost import XGBClassifier
except ImportError:
    print("xgboost not installed — using GradientBoostingClassifier as fallback.")
    XGBClassifier = GradientBoostingClassifier

MODEL_DIR = Path(os.getenv("MODEL_DIR", "/app/models"))
MODEL_DIR.mkdir(parents=True, exist_ok=True)

rng = np.random.RandomState(42)
N = 2000
# 10 football features: home_elo, away_elo, home_form, away_form,
#   odds_home, odds_draw, odds_away, home_goals_avg, away_goals_avg, h2h_home_wins
X = rng.rand(N, 10).astype(np.float32)
# 3-class target: 0=home, 1=draw, 2=away
y3 = rng.choice([0, 1, 2], size=N, p=[0.45, 0.25, 0.30])
# binary target: 0=no, 1=yes
y2 = rng.choice([0, 1], size=N, p=[0.55, 0.45])

# ── 3-class models ───────────────────────────────────────────────────────────
_xgb_kwargs = dict(n_estimators=50, max_depth=4, random_state=42, eval_metric="mlogloss")
if XGBClassifier is not GradientBoostingClassifier and hasattr(XGBClassifier, "use_label_encoder"):
    _xgb_kwargs["use_label_encoder"] = False

MODELS_3CLASS = {
    "xgb_v1":         XGBClassifier(**_xgb_kwargs) if XGBClassifier is not GradientBoostingClassifier
                      else GradientBoostingClassifier(n_estimators=50, random_state=42),
    "rf_v1":          RandomForestClassifier(n_estimators=50, random_state=42),
    "gbm_v1":         GradientBoostingClassifier(n_estimators=50, random_state=42),
    "logistic_v1":    LogisticRegression(max_iter=500, random_state=42),
    "transformer_v1": MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=200, random_state=42),
    "lstm_v1":        MLPClassifier(hidden_layer_sizes=(128, 64, 32), max_iter=200, random_state=42),
    "bayes_v1":       GaussianNB(),
    "dixon_coles_v1": GaussianNB(),
    "market_v1":      GradientBoostingClassifier(n_estimators=30, random_state=42),
    "hybrid_v1":      RandomForestClassifier(n_estimators=80, random_state=42),
    "ensemble_v1":    RandomForestClassifier(n_estimators=100, random_state=42),
}

# ── 2-class models ───────────────────────────────────────────────────────────
_xgb2_kwargs = dict(n_estimators=50, max_depth=3, random_state=42, eval_metric="logloss")
if XGBClassifier is not GradientBoostingClassifier and hasattr(XGBClassifier, "use_label_encoder"):
    _xgb2_kwargs["use_label_encoder"] = False

MODELS_2CLASS = {
    "btts_v2":          XGBClassifier(**_xgb2_kwargs) if XGBClassifier is not GradientBoostingClassifier
                        else GradientBoostingClassifier(n_estimators=50, random_state=42),
    "over_under_v2":    XGBClassifier(**_xgb2_kwargs) if XGBClassifier is not GradientBoostingClassifier
                        else GradientBoostingClassifier(n_estimators=50, random_state=42),
    "correct_score_v2": RandomForestClassifier(n_estimators=50, random_state=42),
}

# ── Rating models (elo / poisson) ─────────────────────────────────────────────
MODELS_RATING = {
    "elo_v1":     RatingShim(),
    "poisson_v1": RatingShim(),
}

trained = 0
errors  = 0

for name, clf in MODELS_3CLASS.items():
    try:
        clf.fit(X, y3)
        path = MODEL_DIR / f"{name}.pkl"
        joblib.dump(clf, path)
        print(f"  ✓ {name} → {path}")
        trained += 1
    except Exception as e:
        print(f"  ✗ {name}: {e}", file=sys.stderr)
        errors += 1

for name, clf in MODELS_2CLASS.items():
    try:
        clf.fit(X, y2)
        path = MODEL_DIR / f"{name}.pkl"
        joblib.dump(clf, path)
        print(f"  ✓ {name} → {path}")
        trained += 1
    except Exception as e:
        print(f"  ✗ {name}: {e}", file=sys.stderr)
        errors += 1

for name, clf in MODELS_RATING.items():
    try:
        clf.fit(X, y2.astype(float))
        path = MODEL_DIR / f"{name}.pkl"
        joblib.dump(clf, path)
        print(f"  ✓ {name} → {path}")
        trained += 1
    except Exception as e:
        print(f"  ✗ {name}: {e}", file=sys.stderr)
        errors += 1

print(f"\nSeeded {trained}/16 models to {MODEL_DIR}")
if errors:
    print(f"WARNING: {errors} model(s) failed to seed.", file=sys.stderr)
    sys.exit(1)
