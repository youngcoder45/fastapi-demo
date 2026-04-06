"""When We need to send data to the api via your client, we send as a request body."""

# A request body is data sent by client to your api
# A response is data sent by api to the client
#
#
# Your API almost always has to send a response body. But clients don't necessarily need to send request bodies all the time, sometimes they only request a path, maybe with some query parameters, but don't send a body.
#
# remember as tim tut said body is optional*
#
# to send data we use POST/ PUT/ DELETE/ PATCH
# exmaple case
from fastapi import FastAPI

# FIrst import BaseModel from Pydantic
from pydantic import BaseModel


# define datamodel as a class that inherits from basemodel
# The same way as defining query paramters , ie if deafult value then it is optional.
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


# here we dfeine a JSON object for python dict like
# {
#     "name": "Foo",
#     "description": "An optional description",
#     "price": 45.2,
#     "tax": 3.5
# } (Desc and tax are optional)

app = FastAPI()


@app.post("/items/")
# now here we are declaring our datamodel as a parameter
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


# Results¶

# With just that Python type declaration, FastAPI will:

#     Read the body of the request as JSON.
#     Convert the corresponding types (if needed).
#     Validate the data.
#         If the data is invalid, it will return a nice and clear error, indicating exactly where and what was the incorrect data.
#     Give you the received data in the parameter item.
#         As you declared it in the function to be of type Item, you will also have all the editor support (completion, etc) for all of the attributes and their types.
#     Generate JSON Schema definitions for your model, you can also use them anywhere else you like if it makes sense for your project.
#     Those schemas will be part of the generated OpenAPI schema, and used by the automatic documentation UIs.


# You can declare path parameters and request body at the same time.
# FastAPI will recognize that the function parameters that match path parameters should be taken from the path, and that function parameters that are declared to be Pydantic models should be taken from the request body.
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.model_dump()}


# You can also declare body, path and query parameters, all at the same time.
# FastAPI will recognize each of them and take the data from the correct place.
@app.put("/items/{item_id}")
async def update_items(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result
