class ModerationClient:
    """
    This client tasks to the Moderation service
    """
    async def get_fragment_has_foul_language(self, sentence: str) -> bool:
        """
        Given a fragment (single sentence) return whether or not
        it contains foul language

        NOTE: This is currently faked out

        If I had access to the real service, I would do a POST using httpx/aiohttp
        as follows:

        curl -X 'POST' \
            'http://content-moderation.service/sentences/' \
            -H 'accept: application/json' \
            -H 'Content-Type: application/json' \
            -d '{
            "fragment": <sentence>,
        }'
        """
        return "frick" in sentence.lower()
