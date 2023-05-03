import sys
sys.path.append('/var/www/mongo-logs-api/data_models/')
import bcrypt
import bson
from bson.json_util import dumps
from pydantic import BaseModel, ValidationError
from typing import Union, Dict, Any
from typing_extensions import Annotated
from fastapi import FastAPI, Request, Body, HTTPException, status, Depends
from price_change import PriceChange
from user_action import UserAction
from data_models.models import find_client_model
from database.mongo import MongoDB
from pprint import pprint
from fastapi.encoders import jsonable_encoder
from pymongo.errors import DuplicateKeyError
from client import ClientSchema, ClientLoginSchema
from auth.auth_handler import signJWT, decodeJWT, hash_password
from auth.auth_bearer import JWTBearer
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from decouple import config
from urllib.parse import parse_qs

app = FastAPI()

db = MongoDB()

def check_client(data: ClientLoginSchema):
    return db.collection("clients").find_one({'email': data.email, 'password': hash_password(data.password)})

def make_query(q: Dict):
    keys = q.keys()

    if "_id" in keys:
      q["_id"] = bson.ObjectId(q["_id"])

    return q

# Routes

@app.post("/client/login", tags=["Client"])
async def client_login(login: ClientLoginSchema = Body(...)):
    client = check_client(login)

    if client:
        id = str(client["_id"])
        repository = client["repository"]
        permission = client["permission"]

        return signJWT(id, repository, permission)
    raise HTTPException(status_code=401, detail="Wrong login details!")

@app.post("/log/{collection}", dependencies=[Depends(JWTBearer())], tags=["Logging"])
def store_log(collection: str, item: Dict[str, Any] = Body(...)):
    try:
        model = find_client_model(collection)

        if model == None:
            raise HTTPException(status_code=404, detail=f"Collection {collection} not found")

        # Validate the request data using the model
        item = model(**item)
    except ValidationError as e:
        # Return a 422 Unprocessable Entity response if the request data is invalid
        raise HTTPException(status_code=422, detail=str(e))

    result = db.collection(collection).insert_one(jsonable_encoder(item))

    return {"message": "_id: {doc_id}".format(doc_id=result.inserted_id)}

@app.post("/select/{collection}", dependencies=[Depends(JWTBearer())], tags=["Logging"])
def logs(collection: str, page: Union[int, None] = 1, limit: Union[int, None] = 2000, q: Dict[str, Any] = Body(...)):
    total = None

    total = db.collection(collection).count_documents(q)
    result = db.collection(collection).find(q).skip(limit*(page-1)).limit(limit)

    result = list(result)
    result = dumps(result)

    return {"result": result, "page": page, "limit": limit, "total": total}
