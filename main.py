from typing import List, Optional, Set, Union, Dict
from enum import Enum
from fastapi import Depends, Cookie, Body, FastAPI, Path, Query, Header, status, Form, File, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, HttpUrl, EmailStr

app = FastAPI()

class Item(BaseModel):
    name: str = Field(..., example="Foo")
    description: Optional[str] = Field(
        None, title="The description of the item", max_length=300, example="A very nice Item"
    )
    price: float = Field(..., gt=0, description="The price must be greater than zero", example=35.4)
    tax: Optional[float] = Field(None, example=3.2)
    tags: List[str] = []
    images: Optional[List[Image]] = None

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass


class UserInDB(UserBase):
    hashed_password: str

items = {"foo": "The Foo Wrestlers"}

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    return items[item_id]

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if (item_id not in items):
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}


@app.delete("/items/{item_id}")
async def read_item(item_id: str):
    if (item in items):
        del items[item]


@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved

@app.get("/users/{user_id}, response_model=UserOut")
async def read_user(user_id: str):
    return {"user_id": user_id}

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Optional[str] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item