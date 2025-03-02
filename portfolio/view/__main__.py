from lib.common import constants
from lib.common.logger import Logger
from lib.security import authorization

logger = Logger(f'{constants.portfolio_label}.view')

def main(args):
    authorized_user = authorization.verify_header(args)
    if not authorized_user:
        return {'statusCode': 401, 'body': { 'message': 'Unauthorized'}}

    return {'statusCode': 200, 'body': { 'message': f'Called the {constants.portfolio_label} view function'} }


if __name__ == '__main__':
    print(main({'message':'Testing newrelic logging'}))
