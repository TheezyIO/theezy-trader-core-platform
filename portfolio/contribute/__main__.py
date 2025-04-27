import traceback

from lib.common.logger import Logger
from lib.security import authorization
from lib.dao import portfolio, account
from lib.common.utils import validate_all_fields

logger = Logger('portfolio.contribute')

field_validation_list = [
    ('portfolioId', int),
    ('deposit', int)
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

    if args['deposit'] <= 0:
        return {'statusCode': 400, 'body': { 'message': 'Deposit amount must be greater than 0'}}

    try:
        portfolio_dao = portfolio.PortfolioDao()
        portfolio_account_details = portfolio_dao.get_portfolio_and_account_by_user_and_portfolio(authorized_user['sub'], args['portfolioId'])

        if not portfolio_account_details:
            return {
                'statusCode': 404,
                'body': {
                    'message': 'This portfolio does not exist',
                    'status': 'failed'
                }
            }

        if args['deposit'] > portfolio_account_details['account_cash_balance']:
            return {
                'statusCode': 400,
                'body': {
                    'message': 'Insufficient funds',
                    'status': 'failed'
                }
            }

        if args['deposit'] < portfolio_account_details['minimum_deposit']:
            return {
                'statusCode': 422,
                'body': {
                    'message': 'Insufficient deposit amount',
                    'status': 'failed'
                }
            }

        if portfolio_account_details['member_id'] != authorized_user['sub']:
            logger.info('Current user is not portfolio member... adding new member')
            new_member = {
                'portfolio_id': args['portfolioId'],
                'user_id': authorized_user['sub'],
                'contribution': args['deposit'],
                'earnings': 0,
            }
            portfolio_dao.create_portfolio_member(new_member)

        # Portfolio transactions
        new_portfolio_transaction =  {
          'amount': args['deposit'],
          'transaction_type_id': 2,
          'portfolio_balance_id': portfolio_account_details['portfolio_balance_id'],
          'user_id': authorized_user['sub']
        }
        portfolio_dao.create_balance_transaction(new_portfolio_transaction)

        new_balance = {
            'cash': portfolio_account_details['portfolio_cash_balance'] + args['deposit']
        }
        portfolio_dao.update_portfolio_balance(new_balance, portfolio_account_details['portfolio_balance_id'])

        # Account transactions
        account_dao = account.AccountDao()

        new_account_transaction =  {
          'amount': args['deposit'],
          'transaction_type_id': 1,
          'account_balance_id': portfolio_account_details['account_balance_id'],
        }
        account_dao.create_transaction(new_account_transaction)

        account_balance = {
            'cash': portfolio_account_details['account_cash_balance'] - args['deposit'],
            'equity': portfolio_account_details['account_equity_balance'] + args['deposit']
        }
        account_dao.update_balance(account_balance, portfolio_account_details['account_balance_id'])

        # Calculate Contribution Percentage
        # contribution_data = portfolio_dao.get_contributions_for_user(authorized_user['sub'], portfolio_account_details['portfolio_balance_id'])
        #
        # if not contribution_data['total_net_contribution']:
        #     contribution_percentage = 100.0
        # else:
        #     contribution_percentage = (contribution_data['user_net_contribution'] / contribution_data['total_net_contribution']) * 100

        return {
            'statusCode': 200,
            'body': {
                'message': 'Successfully contributed funds to the portfolio',
                'status': 'success',
                # 'contribution_total': contribution_data['user_net_contribution'],
                # 'contribution_percentage': contribution_percentage
            }
        }
    except Exception as e:
        error_traceback = traceback.format_exc()

        return {
            'statusCode': 400,
            'body': {
                'message': f"Internal server error while contributing to portfolio : {str(e)}",
                'status': 'failed',
                'error_details': error_traceback
            }
        }