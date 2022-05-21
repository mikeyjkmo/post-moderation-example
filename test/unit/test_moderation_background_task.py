from moderation_ml_example.moderation_client import ModerationClient
from unittest import mock
from moderation_ml_example.background_tasks import run_post_moderation_loop
from moderation_ml_example.models import Post
import pytest
from moderation_ml_example.repository import InMemoryPostRepository


class FakeModerationClient:
    """
    This client tasks to the Moderation service
    """

    async def get_fragment_has_foul_language(self, sentence: str) -> bool:
        """
        Given a fragment (single sentence) return whether or not
        it contains foul language

        NOTE: This is currently faked out
        """
        return "frick" in sentence.lower()


@pytest.mark.asyncio
async def test_posts_are_moderated_correctly():
    """
    Given a Content Moderation Service that returns
      has_foul_language=True for sentences containing the word "frick"
    When calling run_post_moderation_loop
    Then the unmoderated posts should be moderated correctly
    """
    # Given
    moderation_client = FakeModerationClient()
    repo = InMemoryPostRepository()

    safe_post = Post.new(
        title="hello",
        paragraphs=["well, this is safe.", "this is safe too"],
    )
    await repo.save(safe_post)

    unsafe_post = Post.new(
        title="hello", paragraphs=["well, this is safe.", "this is fricking unsafe"]
    )
    await repo.save(unsafe_post)

    # When
    await run_post_moderation_loop(
        moderation_client=moderation_client,
        repo=repo,
        oneshot=True,
    )

    # Then
    safe_result = await repo.get(safe_post.id)
    assert not safe_result.requires_moderation
    assert not safe_result.has_foul_language

    unsafe_result = await repo.get(unsafe_post.id)
    assert not unsafe_result.requires_moderation
    assert unsafe_result.has_foul_language


@pytest.mark.asyncio
async def test_moderation_is_retried_if_error_occurs():
    """
    Given a Content Moderation Service that initially errors, then returns
      has_foul_language=True for sentences containing the word "frick"
    When calling run_post_moderation_loop
    Then the unmoderated posts should be moderated correctly
    """
    # Given
    moderation_client = mock.AsyncMock(spac=ModerationClient)
    moderation_client.get_fragment_has_foul_language.side_effect = [
        Exception("Some network error"),  # first time an error occurs
        True  # second time it succeeds
    ]

    repo = InMemoryPostRepository()
    unsafe_post = Post.new(
        title="hello", paragraphs=["well, this is safe.", "this is fricking unsafe"]
    )
    await repo.save(unsafe_post)

    # When
    await run_post_moderation_loop(
        moderation_client=moderation_client,
        repo=repo,
        interval_seconds=0,
        oneshot=True,
    )

    # Then
    unsafe_result = await repo.get(unsafe_post.id)
    assert not unsafe_result.requires_moderation
    assert unsafe_result.has_foul_language
