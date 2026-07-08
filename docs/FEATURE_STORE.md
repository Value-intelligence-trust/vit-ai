# Feature Store

The Feature Store is the centralized source for feature definitions and transformations.

## Seeded Features
The store is pre-seeded with core sports features:
- `home_form`
- `away_form`
- `form_diff`
- `attack_diff`
- `defense_diff`

## Endpoints
- `GET /api/v1/features`: List all available features.
- `POST /api/v1/features`: Register a new feature definition.
