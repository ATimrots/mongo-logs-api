import sys
import os

def root_path():
    path = os.path.dirname(os.path.abspath(__file__))
    split_path = path.split("mongo-logs-api/")
    return split_path[0] + "mongo-logs-api/"

sys.path.append(root_path() + 'enums/')

from permission import Permission
from pydantic import BaseModel, Field, EmailStr

class ClientSchema(BaseModel):
    company: str = Field(...)
    repository: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    permission: Permission
    active: bool

    class Config:
        schema_extra = {
            "example": {
                "company": "Student",
                "repository": "student",
                "email": "student@student.com",
                "password": "weakpassword",
                "permission": "rw",
                "active": 1
            }
        }

class ClientLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "student@student.com",
                "password": "weakpassword"
            }
        }
