from uuid import uuid4
import pytest
from moderation_ml_example.repository import InMemoryPostRepository, PostNotFoundError
from moderation_ml_example.models import Post


@pytest.fixture(name="repo")
def inmemory_repo_fixture():
    """
    Tests use the InMemoryPostRepository, but this can be changed to any
    kind of Post Repository
    """
    return InMemoryPostRepository()


@pytest.mark.asyncio
async def test_save_and_get(repo):
    # Given
    new_post = Post.new(title="hello", paragraphs=["one", "two"])
    await repo.save(new_post)

    # When
    result = await repo.get(new_post.id)

    # Then
    assert result == new_post
    # Returned Post should be a copy
    assert result is not new_post


@pytest.mark.asyncio
async def test_get_raises_not_found_error_if_post_not_found(repo):
    with pytest.raises(PostNotFoundError, match="Post.*cannot be found"):
        await repo.get(id=uuid4())


@pytest.mark.asyncio
async def test_save_and_list(repo):
    # Given
    post1 = Post.new(title="hello", paragraphs=["one", "two"])
    post2 = Post.new(title="world", paragraphs=["three", "four"])
    await repo.save(post1)
    await repo.save(post2)

    # When
    result = await repo.list()

    # Then
    assert result == [
        post1,
        post2
    ]


@pytest.mark.asyncio
async def test_list_unmoderated(repo):
    # Given
    post1 = Post.new(title="hello", paragraphs=["one", "two"])
    await repo.save(post1)

    post2 = Post.new(title="world", paragraphs=["three", "four"])
    post2.has_foul_language = True
    post2.requires_moderation = False
    await repo.save(post2)

    # When
    result = await repo.list_unmoderated()

    # Then
    assert result == [post1]
