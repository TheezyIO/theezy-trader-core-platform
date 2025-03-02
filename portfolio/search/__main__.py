from lib.common import constants
from lib.common.logger import Logger
from lib.security import authorization
from lib.services import portfolio

import json

logger = Logger(f'{constants.portfolio_label}.search')

def main(args):
    authorized_user = authorization.verify_header(args)

    if not authorized_user:
        return {'body': {'message': 'Unauthorized'}, 'statusCode': 401}

    portfolio_service = portfolio.PortfolioService(args['http']['headers']['authorization'])
    response = portfolio_service.get_portfolios()
    return {'body': json.dumps(response), 'statusCode': 200 }


if __name__ == '__main__':
    print(main({}))
