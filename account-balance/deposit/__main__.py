from lib.common.logger import Logger
from lib.common.utils import validate_all_fields
from lib.security import authorization
from lib.dao import account


logger = Logger('account-balance.deposit')

field_validation_list = [
    ('amount', int)
]

def main(args):
    logger.info(f'Function invocation started...')

    authorized_user = authorization.verify_header(args)

    if not authorized_user:
        return {'statusCode': 401, 'body': { 'message': 'Unauthorized'}}

    if args['http']['method'] != 'POST':
        return {'statusCode': 405, 'body': { 'message': 'Method not allowed'}}
    
    if not validate_all_fields(field_validation_list, args):
        return {'statusCode': 400, 'body': { 'message': 'Missing or invalid parameters'}}

    if args['amount'] <= 0:
        return {'statusCode': 400, 'body': { 'message': 'Deposit amount must be greater than 0'}}
    
    account_dao = account.AccountDao()

    try:
        account_record = account_dao.get_account_for_user(authorized_user['sub'])

        if not account_record:
            return {
                'statusCode': 404,
                'body': {
                    'message': 'Account Balance record not found',
                    'status': 'failed'
                }
            }

        transaction_body = {
            'amount': args['amount'],
            'transaction_type_id': 3, # TODO: Add Transaction Table DAO for dynamic id lookup
            'account_balance_id': account_record['id']
        }
        account_dao.create_transaction(transaction_body)
        account_dao.update_account({'amount': account_record['cash'] + args['amount']}, account_record['id'])

        return {
            'statusCode': 200,
            'body': {
                'message': 'Successfully deposited funds into account',
                'status': 'success'
            }
        }

    except Exception as e:
        return {
            'statusCode': 400,
            'body': {
                'message': f"Internal server error while viewing account : {str(e)}",
                'status': 'failed'
            }
        }
