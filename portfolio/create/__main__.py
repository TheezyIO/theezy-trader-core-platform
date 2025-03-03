from lib.common.logger import Logger
from lib.security import authorization
from lib.services import portfolio

logger = Logger('portfolio.create')

def main(args):
    logger.info(f'Function invocation started...')

    authorized_user = authorization.verify_header(args)
    if not authorized_user:
        return {'statusCode': 401, 'body': { 'message': 'Unauthorized'}}

    if args['http']['method'] != 'POST':
        return {'statusCode': 405, 'body': { 'message': 'Method not allowed'}}

    logger.info(f'Creating portfolio... {args.get("http")}')
    return {'statusCode': 200, 'body': { 'message': 'Portfolio created successfully'}}