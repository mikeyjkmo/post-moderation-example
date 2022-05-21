develop:
	poetry run uvicorn moderation_ml_example.app:app --reload --host 0.0.0.0

.PHONY: develop
