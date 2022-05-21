from fastapi.testclient import TestClient
from moderation_ml_example.app import app


async def test_save_and_list():
    # Given
    client = TestClient(app)
    result = client.post({"title": "hello", "paragraphs": ["foo", "bar"]})
    new_id = result.json()["id"]

    # When
    result = client.list()

    # Then
    assert result.json() == [
        {
            "id": new_id, "title": "hello", "paragraphs": ["foo", "bar"]
        }
    ]
