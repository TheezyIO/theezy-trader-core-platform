from abc import abstractmethod
from lib.common import constants

import requests


class Service:

    def __init__(self, authorization_token):
        self.authorization_token = authorization_token

    def send_request(self, method, url, params=None, body=None):
        request_url = f'{constants.urls.buildship}{url}'
        headers = {
            'Authorization': self.authorization_token,
            'Content-Type': 'application/json'
        }
        return requests.request(method, request_url, headers=headers, json=body, params=params).json()

    def get(self, url, params):
        return self.send_request('GET', url, params=params)

    def post(self, url, body, params=None):
        return self.send_request('POST', url, body=body, params=params)

    def put(self, url, body, params=None):
        return self.send_request('PUT', url, body=body, params=params)

    def delete(self, url, params=None):
        return self.send_request('DELETE', url, params=params)

    @staticmethod
    def send_response(body, status=200):
        return {
            'headers': {
                # This Access Control Allow Origin will need to be set by an environment variable
                'Access-Control-Allow-Origin':'http://localhost:8888,http://127.0.0.1:8888'
            },
            'statusCode': status,
            'body': body
        }