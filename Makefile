develop:
	poetry run uvicorn moderation_ml_example.app:app --reload --host 0.0.0.0

test:
	poetry run pytest -vvv test

mock-moderation-server:
	poetry run uvicorn moderation_ml_example.mock_moderation_service:app --reload --host 0.0.0.0 --port 5000

.PHONY: develop test mock-moderation-server
