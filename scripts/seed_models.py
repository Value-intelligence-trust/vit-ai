#!/usr/bin/env python3
    """Seed VIT AI model artifacts — runs at Docker build time."""
    import os, joblib, numpy as np
    from pathlib import Path
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.linear_model import LogisticRegression, Ridge
    from sklearn.naive_bayes import GaussianNB
    from sklearn.neural_network import MLPClassifier
    from sklearn.preprocessing import LabelEncoder
    try:
      from xgboost import XGBClassifier
    except ImportError:
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

    MODELS = {
      "xgb_v1":          XGBClassifier(n_estimators=50, max_depth=4, random_state=42, eval_metric="mlogloss", use_label_encoder=False) if hasattr(XGBClassifier, "use_label_encoder") else XGBClassifier(n_estimators=50, max_depth=4, random_state=42, eval_metric="mlogloss"),
      "rf_v1":           RandomForestClassifier(n_estimators=50, random_state=42),
      "gbm_v1":          GradientBoostingClassifier(n_estimators=50, random_state=42),
      "logistic_v1":     LogisticRegression(max_iter=500, random_state=42),
      "transformer_v1":  MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=200, random_state=42),
      "lstm_v1":         MLPClassifier(hidden_layer_sizes=(128, 64, 32), max_iter=200, random_state=42),
      "bayes_v1":        GaussianNB(),
      "dixon_coles_v1":  GaussianNB(),
      "market_v1":       GradientBoostingClassifier(n_estimators=30, random_state=42),
      "hybrid_v1":       RandomForestClassifier(n_estimators=80, random_state=42),
      "ensemble_v1":     RandomForestClassifier(n_estimators=100, random_state=42),
    }
    MODELS_2CLASS = {
      "btts_v2":         XGBClassifier(n_estimators=50, max_depth=3, random_state=42, eval_metric="logloss") if XGBClassifier is not GradientBoostingClassifier else GradientBoostingClassifier(n_estimators=50, random_state=42),
      "over_under_v2":   XGBClassifier(n_estimators=50, max_depth=3, random_state=42, eval_metric="logloss") if XGBClassifier is not GradientBoostingClassifier else GradientBoostingClassifier(n_estimators=50, random_state=42),
      "correct_score_v2": RandomForestClassifier(n_estimators=50, random_state=42),
    }
    # poisson/elo/rating models — wrap Ridge in a classifier-compatible shim
    class RatingShim:
      def __init__(self): self.model = Ridge()
      def fit(self, X, y): self.model.fit(X, y); return self
      def predict_proba(self, X):
          p = np.clip(self.model.predict(X), 0, 1).reshape(-1,1)
          return np.hstack([1-p, p])
      def predict(self, X): return (self.model.predict(X) > 0.5).astype(int)

    MODELS_RATING = {
      "elo_v1":     RatingShim(),
      "poisson_v1": RatingShim(),
    }

    trained = 0
    for name, clf in MODELS.items():
      try:
          clf.fit(X, y3)
          path = MODEL_DIR / f"{name}.pkl"
          joblib.dump(clf, path)
          print(f"  \u2713 {name} -> {path}")
          trained += 1
      except Exception as e:
          print(f"  \u2717 {name}: {e}")

    for name, clf in MODELS_2CLASS.items():
      try:
          clf.fit(X, y2)
          path = MODEL_DIR / f"{name}.pkl"
          joblib.dump(clf, path)
          print(f"  \u2713 {name} -> {path}")
          trained += 1
      except Exception as e:
          print(f"  \u2717 {name}: {e}")

    for name, clf in MODELS_RATING.items():
      try:
          clf.fit(X, y2.astype(float))
          path = MODEL_DIR / f"{name}.pkl"
          joblib.dump(clf, path)
          print(f"  \u2713 {name} -> {path}")
          trained += 1
      except Exception as e:
          print(f"  \u2717 {name}: {e}")

    print(f"Seeded {trained}/16 models to {MODEL_DIR}")
    