from datetime import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="My FastAPI App", version="1.0.0")


class Item(BaseModel):
    name: str
    price: float


# In-memory data (resets when the app restarts)
items = {
    1: {"id": 1, "name": "Laptop", "price": 900.0},
    2: {"id": 2, "name": "Phone", "price": 500.0},
}
next_id = 3


@app.get("/")
def home():
    return {"message": "Hello from my FastAPI app running in Docker!"}


@app.get("/health")
def health():
    return {"status": "ok", "time": datetime.now().isoformat()}


@app.get("/hello/{name}")
def hello(name: str):
    return {"message": f"Hello, {name}!"}


@app.get("/add")
def add(a: float, b: float):
    return {"a": a, "b": b, "sum": a + b}


@app.get("/items")
def list_items():
    return list(items.values())


@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]


@app.post("/items", status_code=201)
def create_item(item: Item):
    global next_id
    new_item = {"id": next_id, **item.model_dump()}
    items[next_id] = new_item
    next_id += 1
    return new_item


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    items[item_id] = {"id": item_id, **item.model_dump()}
    return items[item_id]


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted", "item": items.pop(item_id)}
