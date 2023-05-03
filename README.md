# Audit logs API

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

To set up database execute command:

```
python database/migrations/migrate.py up
```
This command will create system base collections, like `clients`, and also will create all custom collections which is client specific and need 
to be defined in Migration class. You can specify schemas for specific database collections. 
Here is example of `clients` schema settings:

```
{
	"clients": {
		"schema": {
			"$jsonSchema": {
				"bsonType": "object",
				"required": ["company", "repository", "email", "password", "permission", "active"],
				"properties": {
					"company": {"type": "string"},
					"repository": {"type": "string"},
					"email": {"type": "string"},
					"password": {"type": "string"},
					"permission": {"type": "string"},
					"active": {"type": "boolean"}
				}
			}
		},
		"indexes": {
			"unique": [[("repository", ASCENDING), ("email", ASCENDING)]]
		}
	}
}
```
You can add schemas as much You want and run migration up again. Only new collections will be created.

If you want to cancel setup, execute command:

```
python database/migrations/migrate.py down

```
To use API admin need to create client. Claint can be created with command (You will be promt to enter client's data):
```
python database/migrations/migrate.py client
```

Start the server:
```
uvicorn main:app --reload
```

When the application starts, navigate to `http://localhost:8000/docs` and try out the endpoints.

## Disclaimer

Use at your own risk; not a supported MongoDB product
