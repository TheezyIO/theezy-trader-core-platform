from lib.auth0 import jwt
from lib.common import constants
from lib.common.logger import Logger


logger = Logger(f'{constants.portfolio_label}.search')

def main(args):
    if jwt.verify_token('Token'):
        logger.info(args)
        response = {'body': { 'message': f'Called the {constants.portfolio_label} search function'}, 'status': 200 }
    else:
        response = {'body': { 'message': 'Unauthorized'}, 'status': 401}

    return response

if __name__ == '__main__':
    print(main({}))
