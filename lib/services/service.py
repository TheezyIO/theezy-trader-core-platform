from abc import abstractmethod
from lib.common import constants

import requests


class Service:

    def __init__(self, authorization_token):
        self.authorization_token = authorization_token

    def send_request(self, method, url, body=None):
        request_url = f'{constants.urls.buildship}{url}'
        headers = {
            'Authorization': self.authorization_token,
            'Content-Type': 'application/json'
        }
        return requests.request(method, request_url, headers=headers, json=body).json()

    @abstractmethod
    def get(self, url):
        return self.send_request('GET', url)
