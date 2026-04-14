""" """

from contextlib import asynccontextmanager
from sys import executable

from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Post, create_db_and_tables, get_async_session
from app.schemas import PostCreate, PostResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello From Mars"}


@app.get("/items/{itemid}")
async def read_data(itemid: int):
    return {"itemid": itemid}


# Incase item id is NOT int it will give us an error


@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(""),
    session: AsyncSession = Depends(get_async_session),
):
    post = Post(
        caption=caption, url="dummyurl", file_type="photo", file_name="dummyname"
    )
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post


@app.get("/feed")
async def get_feed(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]
    post_data = []
    for post in posts:
        post_data.append(
            {
                "id": str(post.id),
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "file_name": post.file_name,
                "created_at": post.created_at.isoformat(),
            }
        )
        return {"posts": post_data}


# Pydantic
# Pydantic is a Python module for data validation
# You declare the "shape" of the data as classes with attributes.
