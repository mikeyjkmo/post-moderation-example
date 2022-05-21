import asyncio
import logging
from moderation_ml_example.repository import PostRepository
from moderation_ml_example.moderation_client import ModerationClient

logger = logging.getLogger(__name__)


async def run_post_moderation_loop(
    moderation_client: ModerationClient,
    repo: PostRepository,
    interval_seconds=10,
):
    """
    This is an async background task loop that moderates any unmoderated posts
    every 10 seconds
    """
    async def _post_has_foul_language(post):
        """
        Check if a Post contains foul language
        """
        for sentence in post.sentences:
            if await moderation_client.get_fragment_has_foul_language(sentence):
                return True
        return False

    async def _update_unmoderated_posts():
        """
        Loop through all unmoderated posts and moderate them
        """
        posts = await repo.list_unmoderated()
        for post in posts:
            post.has_foul_language = await _post_has_foul_language(post)
            post.requires_moderation = False
            await repo.save(post)

    while True:
        try:
            await _update_unmoderated_posts()
        except Exception:
            logger.exception("An error occurred whilst trying to moderate posts")

        await asyncio.sleep(interval_seconds)
