![main workflow](https://github.com/mongodb-developer/pymongo-fastapi-crud/actions/workflows/main.yml/badge.svg)

# Audit logging API

API to communicate audit logs between source of logs and Mongo database. Based on Python PyMongo and FastAPI.

## Running the server

Set your MongoDB server credentials as a parameters in `.env`.

```
db_host=0.0.0.0
db_port=27017
db_database=
db_username=
db_password=
```

Install the required dependencies:

```
pip install -r requirements.txt
```

Start the server:
```
uvicorn main:app --reload
```

When the application starts, navigate to `http://localhost:8000/docs` and try out the endpoints.

## Disclaimer

Use at your own risk; not a supported MongoDB product
