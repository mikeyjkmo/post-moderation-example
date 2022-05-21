from urllib.parse import urljoin

import httpx
from moderation_ml_example.config import config


class ModerationClient:
    """
    This client tasks to the Moderation service
    """
    async def get_fragment_has_foul_language(self, sentence: str) -> bool:
        """
        Given a fragment (single sentence) return whether or not
        it contains foul language
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                urljoin(base=config.CONTENT_MODERATION_SERVICE_URL, url="/sentences")
            )
            response.raise_for_status()
            return response.json()["hasFoulLanguage"]
