from typing import List, Optional, Set, Union, Dict
from enum import Enum
from fastapi import Depends, Cookie, Body, FastAPI, Path, Query, Header, status, Form, File, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, HttpUrl, EmailStr

app = FastAPI()

class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name

class CommonQueryParams:
    def __init__(self, q: Optional[str] = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

class Tags(Enum):
    items = "items"
    users = "users"

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

class Image(BaseModel):
    url: HttpUrl
    name: str

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


class CartBase(BaseModel):
    id_user: int

class CartUpdate(CartBase):
    id_user: int

class CartCreate(CartBase):
    pass

class Cart(CartBase):
    id_cart: int
    products: Set[str] = set() # lista de produtos unicos

    class Config:
        orm_mode = True

items = {"foo": "The Foo Wrestlers"}
carts = {}
cartproducts = {}


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.put("/items/{item_id}", response_model=Item)
async def create_or_update_item(item_id: str, item: Item):
    if (item_id not in items):
        items[item_id] = {}
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if (item_id not in items):
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return items[item_id]


@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    if (item_id in items):
        del items[item]

@app.put("/carts/", response_model=CartCreate)
async def create_or_update_cart(cart_id: str, cart: Cart):
    if (cart_id not in carts):
        carts[cart_id] = {}
    update_cart_encoded = jsonable_encoder(cart)
    carts[cart_id] = update_cart_encoded
    return update_cart_encoded

@app.delete("/carts/{cart_id}")
async def delete_cart(cart_id: str):
    if (cart_id in carts):
        del carts[cart_id]

@app.get("/carts/{cart_id}")
async def read_item(cart_id: str):
    if (cart_id not in carts):
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return carts[cart_id]

@app.patch("/cart/{cart_id}/product/{product_id}")
async def add_to_cart(cart_id:int, product_id: int):
    if (cart_id not in carts):
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    cartt = carts[cart_id]
    cartt[products].append(product_id)
    carts[cart_id] = cartt
    return 

# remover item carrinho de compras 
# como defino a quantidade de itens que vou remover?
@app.delete("/cart/{cart_id}/product/{product_id}")
async def remove_from_cart(cart_id:int, product_id: int):
    if (cart_id in carts):
        for product in carts[cart_id][products]:
            if product == product_id:
                carts[cart_id][products].remove(product)






    
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