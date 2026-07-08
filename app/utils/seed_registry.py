from app.services.registry import registry
from app.schemas.model import ModelCreate
from app.services.feature_store import feature_store
from app.schemas.feature import FeatureCreate

def seed_models():
    models = [
        "lstm_v1", "hybrid_v1", "transformer_v1", "correct_score_v2",
        "ensemble_v1", "market_v1", "xgb_v1", "elo_v1", "rf_v1",
        "btts_v2", "logistic_v1", "gbm_v1", "dixon_coles_v1",
        "bayes_v1", "poisson_v1", "over_under_v2"
    ]

    for m_id in models:
        provider = "ensemble" if m_id == "ensemble_v1" else "internal"
        model_in = ModelCreate(
            id=m_id,
            name=m_id.replace("_", " ").title(),
            description=f"VIT Core {m_id} model migrated to AI Platform",
            capabilities=["prediction", "inference"],
            provider=provider,
            input_schema={},
            output_schema={},
            initial_version="1.0.0"
        )
        if not registry.get_by_id(m_id):
            registry.register(model_in)

def seed_features():
    features = [
        {"id": "home_form", "name": "Home Team Form", "type": "numeric", "description": "Points earned by home team in last 5 games"},
        {"id": "away_form", "name": "Away Team Form", "type": "numeric", "description": "Points earned by away team in last 5 games"},
        {"id": "form_diff", "name": "Form Difference", "type": "numeric", "description": "home_form - away_form"},
        {"id": "attack_diff", "name": "Attack Difference", "type": "numeric", "description": "Difference in goals scored (last 5)"},
        {"id": "defense_diff", "name": "Defense Difference", "type": "numeric", "description": "Difference in goals conceded (last 5)"}
    ]
    for f in features:
        if not feature_store.get_by_id(f["id"]):
            feature_store.register(FeatureCreate(**f))

if __name__ == "__main__":
    seed_models()
    seed_features()
    from app.services.registry import registry
    print(f"Seeded {len(registry.get_all())} models and {len(feature_store.get_all())} features.")
