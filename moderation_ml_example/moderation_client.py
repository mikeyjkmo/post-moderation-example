class ModerationClient:
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
