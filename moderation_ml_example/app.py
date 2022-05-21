from typing import List
from fastapi import FastAPI
from pydantic.main import BaseModel
from moderation_ml_example.models import Post
from moderation_ml_example.repository import InMemoryPostRepository

app = FastAPI()
repo = InMemoryPostRepository()


class PostCollection(BaseModel):
    posts: List[Post]


class PostCreationPayload(BaseModel):
    title: str
    paragraphs: List[str]


@app.post("/posts")
async def create_post(post: PostCreationPayload) -> Post:
    new_post = Post.new(title=post.title, paragraphs=post.paragraphs)
    await repo.save(new_post)
    return new_post


@app.get("/posts")
async def list_posts() -> PostCollection:
    return PostCollection(posts=await repo.list())
