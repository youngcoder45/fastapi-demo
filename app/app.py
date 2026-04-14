""" """

from contextlib import asynccontextmanager
from sys import executable
from app.images import imagekit
from typing import TypedDict
from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Post, create_db_and_tables, get_async_session
from app.schemas import PostCreate, PostResponse
import shutil
import os
import uuid
import tempfile


class UploadFileRequestOptions(TypedDict, total=False):
    use_unique_file_name: bool
    tags: list[str]


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
    filename = file.filename or f"upload-{uuid.uuid4().hex}"
    suffix = os.path.splitext(filename)[1]
    temp_file_path: str | None = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)

        options: UploadFileRequestOptions = {
            "use_unique_file_name": True,
            "tags": ["backend-upload"],
        }

        with open(temp_file_path, "rb") as f:
            upload_result = imagekit.files.upload(
                file=f,
                file_name=filename,
                **options,
            )

        post = Post(
            caption=caption,
            url=upload_result.url,
            file_type=upload_result.file_type,
            file_name=upload_result.name,
        )
        session.add(post)
        await session.commit()
        await session.refresh(post)
        return post
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    finally:
        try:
            await file.close()
        finally:
            if temp_file_path:
                try:
                    os.unlink(temp_file_path)
                except OSError:
                    pass


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
