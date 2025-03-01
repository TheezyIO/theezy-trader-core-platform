import requests
import os


def verify_token(token=None):
    jwks_uri = os.environ.get('AUTH0_JWKS_URI')
    response = requests.get(jwks_uri)
    print(response.content.decode('utf-8'))
    return bool(token)