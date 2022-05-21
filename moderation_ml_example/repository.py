import abc
from uuid import UUID
from moderation_ml_example.models import Post


class PostNotFoundError(Exception):
    pass


class PostRepository:
    __metaclass__ = abc.ABCMeta

    async def save(self, post: Post) -> None:
        ...

    async def get(self, id: UUID) -> Post:
        ...


class InMemoryPostRepository(PostRepository):
    def __init__(self):
        self._posts = {}

    async def save(self, post: Post) -> None:
        self._posts[post.id] = post.copy()

    async def get(self, id: UUID) -> Post:
        try:
            return self._posts[id]
        except KeyError as exc:
            raise PostNotFoundError(f"Post with id {id} cannot be found") from exc
