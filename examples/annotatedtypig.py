from typing import Annotated


def say_hello(name: Annotated[str, "I am just metadata"]) -> str:
    return f"Hello {name}"
