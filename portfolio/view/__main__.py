from lib.auth0 import jwt
from lib.common import constants
from lib.common.logger import Logger

logger = Logger(f'{constants.portfolio_label}.view')

def main(args):
    if jwt.verify_token('Token'):
        logger.info(args)
        response = {'status': 200, 'body': { 'message': f'Called the {constants.portfolio_label} view function'} }
    else:
        response = {'status': 401, 'body': { 'message': 'Unauthorized'}}

    return response


if __name__ == '__main__':
    print(main({'message':'Testing newrelic logging'}))
