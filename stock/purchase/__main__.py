from lib.common.logger import Logger
from lib.security import authorization
from lib.dao import stock, portfolio
from lib.common.utils import validate_all_fields

field_validation_list = [
    ('amount', int),
    ('portfolioId', str),
    ('stock', dict, [('name', str), ('ticker', str), ('price', int)])
]

logger = Logger('stock.purchase')

def main(args):
    logger.info(f'Function invocation started...')

    authorized_user = authorization.verify_header(args)
    if not authorized_user:
        return {'statusCode': 401, 'body': { 'message': 'Unauthorized'}}

    if args['http']['method'] != 'POST':
        return {'statusCode': 405, 'body': { 'message': 'Method not allowed'}}

    if not validate_all_fields(field_validation_list, args):
        return {'statusCode': 400, 'body': { 'message': 'Missing or invalid parameters'}}

    portfolio_id = args['portfolioId']
    stock_ticker = args['stock']['ticker']
    user_id = authorized_user['sub']

    stock_dao = stock.StockDao()
    portfolio_stock_response = stock_dao.get_portfolio_stock_details(portfolio_id, stock_ticker, user_id)

    if not portfolio_stock_response:
        return {
            'statusCode': 404,
            'body': {
                'status': 'failed',
                'message': f'Stock {stock_ticker} does not exist within this portfolio'
            }
        }

    purchase_amount = args['amount']
    purchase_price = args['stock']['price']
    purchase_total = round(purchase_amount * purchase_price)
    [stock_details] = portfolio_stock_response

    # Stock purchasing should probably happen completely within the context of a portfolio and not bleed into the main account
    if stock_details['portfolio_cash_balance'] < purchase_total:
        return {
            'statusCode': 400,
            'body': {
                'status': 'failed',
                'message': f'Not enough cash in portfolio to purchase {purchase_amount} shares of {stock_ticker}'
            }
        }

    portfolio_balance_id = stock_details['portfolio_balance_id']
    portfolio_balance_transaction = {
        'user_id': user_id,
        'amount': purchase_total,
        'transaction_type_id': 1,
        'portfolio_balance_id': portfolio_balance_id
    }

    portfolio_dao = portfolio.PortfolioDao()
    portfolio_dao.create_balance_transaction(portfolio_balance_transaction)

    portfolio_balance_update = {
        'cash': stock_details['portfolio_cash_balance'] - purchase_total,
        'equity': stock_details['portfolio_equity_balance'] + purchase_total,
    }
    portfolio_dao.update_portfolio_balance(portfolio_balance_update, portfolio_balance_id)

    total_stock_price = round(stock_details['portfolio_stock_amount'] * stock_details['portfolio_stock_average_price'])
    new_stock_amount = stock_details['portfolio_stock_amount'] + purchase_amount
    new_total_stock_price = round(total_stock_price + purchase_total)
    new_stock_average_price = round(new_total_stock_price / new_stock_amount)

    portfolio_stock_id = stock_details['portfolio_stock_id']
    portfolio_stock_transaction = {
        'portfolio_stock_id': portfolio_stock_id,
        'price': purchase_price,
        'amount': purchase_amount,
        'transaction_type_id': 1
    }
    stock_dao.create_transaction(portfolio_stock_transaction)

    portfolio_stock_update = {
        'portfolio_id': portfolio_id,
        'stock_id': stock_details['stock_id'],
        'amount': new_stock_amount,
        'average_price': new_stock_average_price,
    }
    stock_dao.update_portfolio_stock(portfolio_stock_update, portfolio_stock_id)

    return {
        'statusCode': 200,
        'body': {
            'status': 'success',
            'message': 'Stock purchased successfully'
        }
    }
