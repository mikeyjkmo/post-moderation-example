from fastapi.testclient import TestClient
from moderation_ml_example.app import app


def test_save_and_list():
    # Given
    client = TestClient(app)
    result = client.post(
        "/posts", json={"title": "hello", "paragraphs": ["foo", "bar"]}
    )
    new_id = result.json()["id"]

    # When
    result = client.get("/posts")

    # Then
    assert result.json() == {
        "posts": [
            {
                "id": new_id,
                "title": "hello",
                "paragraphs": ["foo", "bar"],
                "has_foul_language": None,
                "requires_moderation": True,
            }
        ]
    }


def test_save_and_get():
    # Given
    client = TestClient(app)
    result = client.post(
        "/posts", json={"title": "hello", "paragraphs": ["foo", "bar"]}
    )
    new_id = result.json()["id"]

    # When
    result = client.get(f"/posts/{new_id}")

    # Then
    assert result.json() == {
        "id": new_id,
        "title": "hello",
        "paragraphs": ["foo", "bar"],
        "has_foul_language": None,
        "requires_moderation": True,
    }
