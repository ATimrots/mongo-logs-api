from sys import exit, path
path.append('../../')
path.append("..")
import bson
from pymongo import MongoClient, ASCENDING
from pydantic import ValidationError
from fastapi import HTTPException
from data_models.client import ClientSchema
from pprint import pprint
from datetime import datetime
from auth.auth_handler import hash_password
import argparse
import getpass
from pymongo.errors import DuplicateKeyError
from fastapi.encoders import jsonable_encoder
from mongo import MongoDB

class Migration:
    # double       double-precision floating-point value
    # string       UTF-8 string
    # object       embedded document (i.e. a dictionary)
    # array        list or array
    # objectId     a MongoDB ObjectId
    # date         datetime object
    # bool         boolean value
    # null         null value
    # regex        regular expression
    # int          32-bit integer
    # timestamp    a special BSON timestamp type
    # long         64-bit integer
    # decimal      decimal128
    # uuid         a universally unique identifier (UUID)
    # binData      binary data
    # mixed        a field that can contain any BSON data type
    base_collections = {
        "clients": {
            'schema': {
                '$jsonSchema': {
                    'bsonType': 'object',
                    'required': ['company', 'repository', 'email', 'password', 'permission', 'active'],
                    'properties': {
                        "company": {'type': 'string'},
                        "repository": {'type': 'string'},
                        "email": {'type': 'string'},
                        "password": {'type': 'string'},
                        "permission": {'type': 'string'},
                        "active": {'type': 'boolean'}
                    }
                }
            },
            # https://www.mongodb.com/docs/v6.0/indexes/
            'indexes': {
                # https://www.mongodb.com/docs/v5.0/core/index-unique/
                'unique': [[("repository", ASCENDING), ("email", ASCENDING)]]
            }
        }
    }

    custom_collections = {
        "price_changes": {
            'schema': {
                '$jsonSchema': {
                    'bsonType': 'object',
                    'required': ['project', 'product_uuid', 'price_type', 'time'],
                    'properties': {
                        "project": {'type': 'string'},
                        "product_uuid": {'type': 'string'},
                        "price_type": {'type': 'string'},
                        "old": {"anyOf": [{'bsonType': 'double'}, {'bsonType': 'null'}]},
                        "new": {"anyOf": [{'bsonType': 'double'}, {'bsonType': 'null'}]},
                        "time": {'type': 'string'}
                    }
                }
            },
            # https://www.mongodb.com/docs/v6.0/indexes/
            'indexes': {
                # https://www.mongodb.com/docs/v5.0/core/index-unique/
                'unique': []
            }
        }
    }

    def __init__(self):
        mongo = MongoDB()
        self.db = mongo.db()

    def collection(self, collection: str):
        return self.db[collection]

    def up(self):
        print("Up migration")

        collections = Migration.base_collections
        collections.update(Migration.custom_collections)

        collist = self.db.list_collection_names()

        for col, settings in collections.items():
            if col in collist:
                print("The collection '{col}' already exists.".format(col=col))
                continue

            # create the collection with the schema
            self.db.create_collection(col, validator=settings["schema"])
            print("Created the collection '{col}'.".format(col=col))

            for field in settings["indexes"]["unique"]:
                db[col].create_index(field, unique=True)

        print("Done!")

    def down(self):
        print("Down migration")

        collections = Migration.base_collections
        collections.update(Migration.custom_collections)

        collist = self.db.list_collection_names()

        for col, settings in collections.items():
            if col not in collist:
                print("The collection '{col}' not found.".format(col=col))
                continue

            # create the collection with the schema
            self.db[col].drop()
            print("Droped the collection '{col}'.".format(col=col))

        print("Done!")

    def create_client(self):
        print('\033[97m'+'Create new client')

        # Request parameters one by one
        company = input('\033[93m'+"Enter company: ")
        repository = input("Enter repository: ")
        email = input("Enter email: ")
        password = getpass.getpass("Enter password: ")
        permission = input("Enter permission: ")
        active = input("Is client active? [1]:") or 1

        print('\033[92m'+"----------- Entered data -----------")
        print('\033[92m'+'company: '+'\033[96m', company)
        print('\033[92m'+'repository: '+'\033[96m', repository)
        print('\033[92m'+'email: '+'\033[96m', email)
        print('\033[92m'+'permission: '+'\033[96m', permission)
        print('\033[92m'+'active: '+'\033[96m', active)

        confirm = input('\033[97m'+"Do You confirm this data? [yes]/no:") or 'yes'

        if confirm != 'yes':
            print('\033[91m'+'Client creation canceled!')
            exit(0)

        data = {
            "company": company,
            "repository": repository,
            "email": email,
            "password": hash_password(password),
            "permission": permission,
            "active": bool(active)
        }

        try:
            client = ClientSchema(**data)
        except ValidationError as e:
            # Return a 422 Unprocessable Entity response if the request data is invalid
            print('\033[91m'+'Validation error: {error}'.format(error=str(e)))
            exit(0)

        try:
            result = self.db["clients"].insert_one(jsonable_encoder(data))
            print('\033[92m'+'Client succesfully created!')
        except DuplicateKeyError as e:
            raise HTTPException(status_code=409, detail=str(e))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('action', nargs='?', choices=['up', 'down', 'client'], help='up/down/client')
    args = parser.parse_args()
    action = args.action

    migration = Migration()

    if action == 'up':
        migration.up()
    elif action == 'down':
        migration.down()
    elif action == 'client':
        migration.create_client()
    else:
        print("One of the action arguments required, choose up, down or client!\n[Example] python migrate.py up")
