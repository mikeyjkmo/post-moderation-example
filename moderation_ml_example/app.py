import asyncio
from moderation_ml_example.moderation_client import ModerationClient

from typing import List
from fastapi import FastAPI
from pydantic.main import BaseModel
from moderation_ml_example.models import Post
from moderation_ml_example.repository import InMemoryPostRepository
from moderation_ml_example.background_tasks import run_post_moderation_loop


class PostCollection(BaseModel):
    posts: List[Post]


class PostCreationPayload(BaseModel):
    title: str
    paragraphs: List[str]


def create_app(repository_factory=InMemoryPostRepository) -> FastAPI:
    """
    Create the FastAPI app

    Defaults to using the InMemoryPostRepository
    """
    app = FastAPI()
    repo = repository_factory()
    background_moderation_task = None

    @app.post("/posts")
    async def create_post(post: PostCreationPayload) -> Post:
        new_post = Post.new(title=post.title, paragraphs=post.paragraphs)
        await repo.save(new_post)
        return new_post

    @app.get("/posts")
    async def list_posts() -> PostCollection:
        return PostCollection(posts=await repo.list())

    @app.on_event("startup")
    async def start_background_tasks():
        nonlocal background_moderation_task
        if not background_moderation_task:
            background_moderation_task = asyncio.create_task(
                run_post_moderation_loop(
                    moderation_client=ModerationClient(),
                    repo=repo,
                )
            )

    @app.on_event("shutdown")
    async def stop_background_tasks():
        if background_moderation_task:
            background_moderation_task.cancel()

    return app


app = create_app()
