develop:
	poetry run uvicorn moderation_ml_example.app:app --reload --host 0.0.0.0

test:
	poetry run pytest -vvv test

.PHONY: develop test
