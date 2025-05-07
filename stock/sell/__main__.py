from lib.common.logger import Logger
from lib.common.utils import validate_all_fields
from lib.security import authorization
from lib.dao import stock, portfolio

field_validation_list = [
    ('amount', int),
    ('portfolioId', str),
    ('stock', dict, [('name', str), ('ticker', str), ('price', int)])
]

logger = Logger('stock.sell')

def main(args):
    logger.info(f'Function invocation started...')

    authorized_user = authorization.verify_header(args)
    if not authorized_user:
        return {'statusCode': 401, 'body': { 'message': 'Unauthorized'}}

    if args['http']['method'] != 'POST':
        return {'statusCode': 405, 'body': { 'message': 'Method not allowed'}}

    if not validate_all_fields(field_validation_list, args):
        return {'statusCode': 400, 'body': { 'message': 'Missing or invalid parameters'}}

    stock_dao = stock.StockDao()
    portfolio_stock_response = stock_dao.get_portfolio_stock_details(args['portfolioId'], args['stock']['ticker'], authorized_user['sub'])

    if not portfolio_stock_response:
        return {
            'statusCode': 404,
            'body': {
                'status': 'failed',
                'message': f'Stock {args["stock"]["ticker"]} does not exist within this portfolio'
            }
        }

    sale_amount = args['amount']
    sale_price = args['stock']['price']
    sale_total = round(sale_amount * sale_price)
    [stock_details] = portfolio_stock_response

    if stock_details['portfolio_stock_amount'] < sale_amount:
        return {
            'statusCode': 400,
            'body': {
                'status': 'failed',
                'message': f'Not enough stock in portfolio to sell {sale_amount} shares of {args["stock"]["ticker"]}'
            }
        }

    portfolio_balance_id = stock_details['portfolio_balance_id']
    portfolio_balance_transaction = {
        'user_id': authorized_user['sub'],
        'amount': sale_total,
        'transaction_type_id': 5,
        'portfolio_balance_id': portfolio_balance_id
    }

    portfolio_dao = portfolio.PortfolioDao()
    portfolio_dao.create_balance_transaction(portfolio_balance_transaction)

    portfolio_balance_update = {
        'cash': stock_details['portfolio_cash_balance'] + sale_total,
        'equity': stock_details['portfolio_equity_balance'] - sale_total,
    }
    portfolio_dao.update_portfolio_balance(portfolio_balance_update, portfolio_balance_id)

    portfolio_stock_id = stock_details['portfolio_stock_id']
    portfolio_stock_transaction = {
        'portfolio_stock_id': portfolio_stock_id,
        'price': sale_price,
        'amount': sale_amount,
        'transaction_type_id': 5
    }
    stock_dao.create_transaction(portfolio_stock_transaction)

    new_stock_amount = stock_details['portfolio_stock_amount'] - sale_amount
    portfolio_stock_update = {
        'portfolio_id': args['portfolioId'],
        'stock_id': stock_details['stock_id'],
        'amount': new_stock_amount
    }
    stock_dao.update_portfolio_stock(portfolio_stock_update, portfolio_stock_id)

    return {
        'statusCode': 200,
        'body': {
            'status': 'success',
            'message': 'Stock sale successful'
        }
    }
