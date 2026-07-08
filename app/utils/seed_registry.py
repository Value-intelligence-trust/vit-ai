from app.services.registry import registry
from app.schemas.model import ModelCreate

def seed_models():
    models = [
        "lstm_v1", "hybrid_v1", "transformer_v1", "correct_score_v2",
        "ensemble_v1", "market_v1", "xgb_v1", "elo_v1", "rf_v1",
        "btts_v2", "logistic_v1", "gbm_v1", "dixon_coles_v1",
        "bayes_v1", "poisson_v1", "over_under_v2"
    ]

    for m_id in models:
        model_in = ModelCreate(
            id=m_id,
            name=m_id.replace("_", " ").title(),
            version="1.0.0",
            description=f"VIT Core {m_id} model migrated to AI Platform",
            capabilities=["prediction", "inference"],
            provider="internal",
            input_schema={},
            output_schema={},
            status="active"
        )
        if not registry.get_by_id(m_id):
            registry.register(model_in)

if __name__ == "__main__":
    seed_models()
    print(f"Seeded {len(registry.get_all())} models.")
