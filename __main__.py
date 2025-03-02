from portfolio.search import __main__ as portfolio_search
from portfolio.view import __main__ as portfolio_view
from lib.common.logger import Logger

logger = Logger('Application.main')

def main(args):
    print(portfolio_search.main(args))
    print(portfolio_view.main(args))
    return {'status': 200}


if __name__ == '__main__':
    logger.info('Starting application...')
    main({'message': 'Testing newrelic logging'})

