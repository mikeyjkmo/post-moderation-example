import abc
from typing import Dict, List
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

    async def list(self) -> List[Post]:
        ...

    async def list_unmoderated(self) -> List[Post]:
        ...


class InMemoryPostRepository(PostRepository):
    def __init__(self):
        self._posts: Dict[UUID, Post] = {}

    async def save(self, post: Post) -> None:
        self._posts[post.id] = post.copy()

    async def get(self, id: UUID) -> Post:
        try:
            return self._posts[id]
        except KeyError as exc:
            raise PostNotFoundError(f"Post with id {id} cannot be found") from exc

    async def list(self) -> List[Post]:
        return [post.copy() for post in self._posts.values()]

    async def list_unmoderated(self) -> List[Post]:
        return [
            post.copy()
            for post in self._posts.values()
            if post.requires_moderation
        ]
