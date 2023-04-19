from price_change import PriceChange
from user_action import UserAction
from auth.auth_bearer import JWTBearer
from auth.auth_handler import decodeJWT
from pprint import pprint

# Define available collections for each client. Key is repository from client object.
models = {
    'student' : {
        'user_actions': UserAction,
        'price_changes': PriceChange
    }
}


def find_client_model(collection: str):
    token = JWTBearer().get_token()
    token_data = decodeJWT(token)
    repository = token_data['repository']

    if repository not in models:
        return None

    collections = models[repository]

    if collection not in collections:
        return None

    return models[repository][collection]
