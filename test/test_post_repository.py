from uuid import uuid4
import pytest
from moderation_ml_example.repository import InMemoryPostRepository, PostNotFoundError
from moderation_ml_example.models import Post


@pytest.mark.asyncio
async def test_save_and_get():
    # Given
    repo = InMemoryPostRepository()
    new_post = Post.new(title="hello", paragraphs=["one", "two"])
    await repo.save(new_post)

    # When
    result = await repo.get(new_post.id)

    # Then
    assert result == new_post
    # Returned Post should be a copy
    assert result is not new_post


@pytest.mark.asyncio
async def test_get_raises_not_found_error_if_post_not_found():
    # Given
    repo = InMemoryPostRepository()

    # When, Then
    with pytest.raises(PostNotFoundError, match="Post.*cannot be found"):
        await repo.get(id=uuid4())
