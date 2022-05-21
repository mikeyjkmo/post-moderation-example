import itertools
from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel


class Post(BaseModel):
    id: UUID
    title: str
    paragraphs: List[str]
    has_foul_language: Optional[bool]
    requires_moderation: bool = True

    @classmethod
    def new(cls, title: str, paragraphs: List[str]):
        return Post(
            id=uuid4(),
            title=title,
            paragraphs=paragraphs,
        )

    @property
    def sentences(self) -> List[str]:
        return list(itertools.chain.from_iterable(
            [
                paragraph.split(".") for paragraph in self.paragraphs
            ]
        ))


class PostNotFoundError(Exception):
    pass
