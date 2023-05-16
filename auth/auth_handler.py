from sys import path
import os

def root_path():
    path = os.path.dirname(os.path.abspath(__file__))
    split_path = path.split("mongo-logs-api/")
    return split_path[0] + "mongo-logs-api/"

path.append(root_path() + 'data_models/')

import time
import bcrypt
import jwt
from typing import Dict
from decouple import config
from pprint import pprint
from client import ClientSchema

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

PASSWORD_SALT = config("password_salt").encode('utf-8')

def token_response(token: str):
    return {"access_token": token}

def signJWT(id: str, rep: str, permission: str):
    payload = {
        "_id": id,
        "repository": rep,
        "permission": permission,
        "expires": time.time() + 28800
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)

def decodeJWT(token: str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}

def hash_password(password_str: str):
    hash = bcrypt.hashpw(password_str.encode('utf-8'), PASSWORD_SALT)

    return hash.decode('utf-8')
