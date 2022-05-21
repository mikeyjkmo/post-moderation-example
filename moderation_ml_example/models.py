from typing import List
from uuid import UUID, uuid4
from pydantic import BaseModel


class Post(BaseModel):
    id: UUID
    title: str
    paragraphs: List[str]

    @classmethod
    def new(cls, title: str, paragraphs: List[str]):
        return Post(
            id=uuid4(),
            title=title,
            paragraphs=paragraphs,
        )


class PostNotFoundError(Exception):
    pass
