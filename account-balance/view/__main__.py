from lib.common.logger import Logger
from lib.security import authorization
from lib.dao import account
from datetime import datetime


logger = Logger('account-balance.view')

def main(args):
    logger.info(f'Function invocation started...')

    authorized_user = authorization.verify_header(args)

    if not authorized_user:
        return {'statusCode': 401, 'body': { 'message': 'Unauthorized'}}

    if args['http']['method'] != 'GET':
        return {'statusCode': 405, 'body': { 'message': 'Method not allowed'}}
    
    
    account_dao = account.AccountDao()
    
    try:
        account_record = account_dao.get_account_for_user(authorized_user['sub'])
        
        if not account_record:
            account_dao.create_account(authorized_user['sub'])
            return {
                'statusCode': 200,
                'body': {
                    'cashBalance': 0,
                    'equityBalance': 0,
                    'timestamp': datetime.now()
                }
            }
        else:
            return {
                'statusCode': 200,
                'body': {
                    'cashBalance': account_record['cash'],
                    'equityBalance': account_record['equity'],
                    'timestamp': str(account_record['modified_at'])
                }
            }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': {
                'message': f"Internal server error while viewing account for {authorized_user['sub']} : {str(e)}",
                'status': 'failed'
            }
        }
