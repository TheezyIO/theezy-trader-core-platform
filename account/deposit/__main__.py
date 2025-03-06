from lib.common.logger import Logger
from lib.security import authorization
from lib.services import account


logger = Logger('account.deposit')

def main(args):
    logger.info(f'Function invocation started...')

    authorized_user = authorization.verify_header(args)

    if not authorized_user:
        return {'statusCode': 401, 'body': { 'message': 'Unauthorized'}}

    if args['http']['method'] != 'POST':
        return {'statusCode': 405, 'body': { 'message': 'Method not allowed'}}

    if 'amount' not in args:
        return {'statusCode': 400, 'body': { 'message': 'Missing or invalid parameters'}}

    account_service = account.AccountService(args['http']['headers']['authorization'])
    response = account_service.deposit_funds(args['amount'])

    return {'statusCode': 200, 'body': response}
