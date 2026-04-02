# Import FastAPI
from fastapi import FastAPI

# Create a fastapi Instance

app = FastAPI()


# Create a Path Operation
# Path aka Route or Endpoint is the URL where We want our API to work.
@app.get("/")
async def root():
    return {"message": "Hola Amingo"}


@app.get("/items/{itemid}")
async def read_data(itemid: int):
    return {"itemid": itemid}


# We can return like A dictionary, list, string, integer or a PYDANTIC MODULE

# while building an api the path is the main way to separate Resources and Concerns
#
# OPERATION
# Operation refers to one of the HTTPS Methods (CRUD PRINCIPLE)
# 1. Post -> Create data
# 2. Get -> Read Data
# 3. put -> Update data
# 4. Delete -> Delete data
# 5. Head
# 6. Options
# 7. Patch
# 8. Trace


# The parts or a URL
# https://pages.fastapi.com/docs/12232?skip=06&limit=1
# https:// -> Schema
# pages -> Subdomain
# fastapi.com -> Domain
# fastapi -> domain Name
# .com -> Top tier Domain
# docs -> Path/Endpoint/Route
# 12232 -> Path Parameter
# ?skip=06%limit=1 -> Query Parameter
#
# PATH PARAMETER
#
# example code can be like
# @app.get("/docs/{docid}")
# async def read_data(docid):
#     return {"id": docid}

# we can ofcourse obviously declare types of path parameters like int/string etc
# In case of datatype mismatch we get a beautiful error
# {"detail":[{"type":"int_parsing","loc":["path","itemid"],"msg":"Input should be a valid integer, unable to parse string as an integer","input":"foo"}]}


# in path order always matters
# ex.
#
# @app.get("/users/me")
# async def read_user_me():
#     return {"user_id": "the current user"}
# @app.get("/users/{user_id}")
# async def read_user(user_id: str):
#     return {"user_id": user_id}

# Otherwise, the path for /users/{user_id} would match also for /users/me, "thinking" that it's receiving a parameter user_id with a value of "me


# Query Parameter
# Any function parameter other than the PATH id parameter is Query paraamter like
#
# @app.get("/post/{postid}")
# async def funcname(postid:int, sequence:int):
#   pass
# here
# postid -> Path parameter
# sequence -> Query parameter
#
# We can also set default values of query paramter here like
# sequence:int = 0
# set the value of a parameter as NONE to make it optional (remember to make a type annotation for none as welll as other one like:)
# def func(parameter:str | None = None):
#   pass
# here the paramter is optional
