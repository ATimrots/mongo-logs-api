import sys
sys.path.append('/var/www/mongo-log-api/data_models/')

import bcrypt

from pydantic import BaseModel, ValidationError
from typing import Union, Dict, Any
from fastapi import FastAPI, Request, Body, HTTPException, status, Depends
from price_change import PriceChange
from user_action import UserAction
from models import models
from database.mongo import MongoDB
from pprint import pprint
from fastapi.encoders import jsonable_encoder

from pymongo.errors import DuplicateKeyError

from client import ClientSchema, ClientLoginSchema
from auth.auth_handler import signJWT, decodeJWT, hash_password
from auth.auth_bearer import JWTBearer

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from decouple import config

app = FastAPI()

db = MongoDB()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

def check_client(data: ClientLoginSchema):
    return db.collection("clients").find_one({'email': data.email, 'password': hash_password(data.password)})

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/client/signup", tags=["Client"])
async def create_client(client: ClientSchema = Body(...)):
    client.password = hash_password(client.password)

    try:
        result = db.collection("clients").insert_one(jsonable_encoder(client))
        return {"message": "Client created _id: {doc_id}".format(doc_id=result.inserted_id)}
    except DuplicateKeyError as e:
        raise HTTPException(status_code=409, detail=str(e))

@app.post("/client/login", tags=["Client"])
async def client_login(login: ClientLoginSchema = Body(...)):
    client = check_client(login)

    if client:
        id = str(client["_id"])
        repository = client["repository"]
        permission = client["permission"]

        return signJWT(id, repository, permission)
    return {"error": "Wrong login details!"}

@app.post("/log/{collection}", dependencies=[Depends(JWTBearer())], tags=["Logging"])
def store_log(collection: str, item: Dict[str, Any] = Body(...)):
    try:
        model = models.get(collection)

        if model == None:
            raise HTTPException(status_code=404, detail=f"Collection {collection} not found")

        # Validate the request data using the model
        item = model(**item)
    except ValidationError as e:
        # Return a 422 Unprocessable Entity response if the request data is invalid
        raise HTTPException(status_code=422, detail=str(e))

    result = db.collection(collection).insert_one(jsonable_encoder(item))

    return {"message": "_id: {doc_id}".format(doc_id=result.inserted_id)}
