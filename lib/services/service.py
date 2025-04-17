from lib.common import constants
from lib.common.logger import Logger

import requests


logger = Logger('services.service')


class Service:

    def __init__(self, authorization_token, base_url=constants.urls.buildship):
        self.base_url = base_url
        self.authorization_token = authorization_token
        self.status_code = 200

    def send_request(self, method, url, params=None, body=None):
        request_url = f'{self.base_url}{url}'
        headers = {
            'Authorization': self.authorization_token,
            'Content-Type': 'application/json'
        }
        logger.debug(f'[{method}] {request_url}')
        if body:
            logger.debug(f'Request body: {body}')
        response = requests.request(method, request_url, headers=headers, json=body, params=params)
        self.status_code = response.status_code
        return response.json()

    def get(self, url, params=None):
        return self.send_request('GET', url, params=params)

    def post(self, url, body, params=None):
        return self.send_request('POST', url, body=body, params=params)

    def put(self, url, body, params=None):
        return self.send_request('PUT', url, body=body, params=params)

    def delete(self, url, params=None):
        return self.send_request('DELETE', url, params=params)

    def send_response(self, body, status=None):
        logger.debug(f'Response status={self.status_code} body={body}')
        return {'statusCode': status if status else self.status_code, 'body': body}
