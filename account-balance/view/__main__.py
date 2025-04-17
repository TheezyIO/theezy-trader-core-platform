from lib.common.logger import Logger
from lib.security import authorization
from lib.services import account


logger = Logger('account-balance.view')

def main(args):
    logger.info(f'Function invocation started...')

    authorized_user = authorization.verify_header(args)

    if not authorized_user:
        return {'statusCode': 401, 'body': { 'message': 'Unauthorized'}}

    if args['http']['method'] != 'GET':
        return {'statusCode': 405, 'body': { 'message': 'Method not allowed'}}

    account_service = account.AccountService(args['http']['headers']['authorization'])
    response = account_service.get_balance()

    return account_service.send_response(response)
