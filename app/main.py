from uuid import UUID, uuid4

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import Response
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND


class Item(BaseModel):
    id: UUID = uuid4()
    name: str
    price: float
    tax: float
    description: str = None


app = FastAPI()

items = {}


@app.get("/")
def read_root(user: str = "World"):
    return {"Hello": user}


@app.get("/item")
def get_items(response: Response):
    response.status_code = HTTP_200_OK if len(items) > 0 else HTTP_204_NO_CONTENT
    return list(items.values()) if len(items) > 0 else None


@app.post("/item", status_code=HTTP_201_CREATED)
def create_item(item: Item):
    items[item.id] = item
    return item


@app.get("/item/{item_id}")
def get_item(item_id: UUID, response: Response):
    item = items.get(item_id)
    response.status_code = HTTP_200_OK if item else HTTP_404_NOT_FOUND
    return item


@app.put("/item/{item_id}")
def put_item(item_id: UUID, item: Item, response: Response):
    item.id = item_id
    existing = items.get(item_id)
    if existing:
        del items[item_id]
        response.status_code = HTTP_200_OK
    else:
        response.status_code = HTTP_201_CREATED
    items[item_id] = item
    return item


@app.delete("/item/{item_id}")
def delete_item(item_id: UUID, response: Response):
    item = items.get(item_id)
    response.status_code = HTTP_200_OK if item else HTTP_404_NOT_FOUND
    if item:
        del items[item_id]
    return item
