import bson
from pymongo import MongoClient, ASCENDING
from pprint import pprint
from datetime import datetime
from sys import exit, path
import argparse

path.append("..")

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('action', nargs='?', choices=['up', 'down'], help='up or down')
    args = parser.parse_args()
    action = args.action

    migration = Migration()

    if action == 'up':
        migration.up()
    elif action == 'down':
        migration.down()
    else:
        print("One of the action arguments required, choose up or down!\n[Example] python migrate.py up")
