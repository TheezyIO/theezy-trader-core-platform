from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend
from lib.common.logger import Logger

import requests
import jwt
import os


logger = Logger('security.authorization')

def validate_jwt_token(authorization_token):
    [_,jwt_token] = authorization_token.split(' ')
    jwks_uri = os.getenv('AUTH0_JWKS_URI')
    audience = os.getenv('AUTH0_AUDIENCE')
    response = requests.get(jwks_uri)

    try:
        logger.debug(f'Validating JWT token: {jwt_token}')
        public_key = load_pem_x509_certificate(response.content, default_backend()).public_key()
        validated_token = jwt.decode(jwt_token, public_key, algorithms=['RS256'], audience=audience)
        return validated_token
    except jwt.exceptions.DecodeError as e:
        logger.error(f'JWT token validation failed: {e}')
        return None
    except jwt.exceptions.ExpiredSignatureError as e:
        logger.error(f'JWT token has expired: {e}')
        return None


def verify_header(request):
    if 'http' not in request or 'headers' not in request['http']:
        logger.error('Http metadata missing from request')
        return None

    http_headers = request['http']['headers']
    if 'authorization' not in http_headers:
        logger.error('Authorization header missing from http request metadata')
        return None

    if 'Bearer' in http_headers['authorization']:
        return validate_jwt_token(http_headers['authorization'])

    return None