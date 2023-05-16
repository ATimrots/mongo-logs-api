import bson
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime
from sys import exit
from decouple import config

class MongoDB:
    def __init__(self):
        self.client = MongoClient(
            MongoDB.DB_HOST,
            int(MongoDB.DB_PORT),
            username=MongoDB.DB_USERNAME,
            password=MongoDB.DB_PASSWORD,
            authSource=MongoDB.DB_DATABASE,
            authMechanism='SCRAM-SHA-1')

        self.client = MongoClient(
            MongoDB.DB_HOST,
            int(MongoDB.DB_PORT))

        # self.readWrite = MongoClient('0.0.0.0', 27017, username='auditor', password='auditor', authSource='audit', authMechanism='SCRAM-SHA-1')
        # self.read = MongoClient('0.0.0.0', 27017, username='auditor', password='auditor', authSource='audit', authMechanism='SCRAM-SHA-1')

    def db(self):
        return self.client[MongoDB.DB_DATABASE]

    def collection(self, collection: str):
        return self.db()[collection]

    def test(self):
        # # List all the databases in the cluster:
        # for db_info in client.list_database_names():
        #    print(db_info)

        # Get a reference to the 'audit' database:
        db = self.client['audit']

        # List all the collections in 'logs':
        collections = db.list_collection_names()
        for collection in collections:
           print(collection)

        user_actions = db['user_actions']

        # Get the document with the model_uuid '0c5cfb9a-258a-4072-b0a7-957a428e555a':
        pprint(user_actions.find_one({'model_uuid': '0c5cfb9a-258a-4072-b0a7-957a428e555a'}))

        # Insert a document for the api_logs 'Parasite':
        insert_result = user_actions.insert_one({
            "code": 200,
            "created_at": datetime(2023, 3, 27, 22, 5, 6),
            "data": {"title": "Some product title"},
            "direction": "incoming",
            "method": "PUT",
            "model_uuid": "0c5cfb9a-258a-4072-b0a7-957a428e555a",
            "project": "inserv",
            "response": None,
            "url": "/api/products/0c5cfb9a-258a-4072-b0a7-957a428e555a"
            })

        # Save the inserted_id of the document you just created:
        doc_id = insert_result.inserted_id
        print("_id of inserted document: {doc_id}".format(doc_id=doc_id))

        # Look up the document you just created in the collection:
        pprint(user_actions.find_one({'_id': bson.ObjectId(doc_id)}))
        user_actions
        # Look up the api_logs:
        for doc in user_actions.find({"model_uuid": "0c5cfb9a-258a-4072-b0a7-957a428e555a"}):
           pprint(doc)

        update_id = bson.ObjectId("64367f2a238b038fb6f0e588")
        # Update the document with the correct title:
        update_result = user_actions.update_one({ '_id': update_id }, {
           '$set': {"data.title": "Some product title EDITED"}
        })
        # Print out the updated record to make sure it's correct:
        pprint(user_actions.find_one({'_id': update_id}))

        # Delete documents
        user_actions.delete_one({"_id": update_id})

        # Delete documents
        user_actions.delete_many({"data.title": "Some product title EDITED"})
