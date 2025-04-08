from lib.common.logger import Logger
from lib.common.utils import validate_all_fields
from lib.security import authorization
from lib.services import user

logger = Logger('user')

field_validation_list = [
    ('id', str),
    ('name', str),
    ('username', str),  # might remove
    ('email', str),     # might remove
]

def main(args):
    logger.info(f'Function invocation started...')

    # Going to leave authorization logic in, since this will be a post Auth0 process
    authorized_user = authorization.verify_header(args)
    if not authorized_user:
        return {'statusCode': 401, 'body': { 'message': 'Unauthorized'}}

    if args['http']['method'] != 'POST':
        return {'statusCode': 405, 'body': { 'message': 'Method not allowed'}}
    
    if not validate_all_fields(field_validation_list, args):
        return {'statusCode': 400, 'body': { 'message': 'Missing or invalid parameters'}}

    user_service = user.UserService(args['http']['headers']['authorization'])
    
    request_body = {
        'id': args['id'],
        'name': args['name'],
        'username': args['username'],
        'email': args['email'],
    }
    
    logger.info(f'Creating user... {request_body}')
    response = user_service.create_user(request_body)

    return user_service.send_response(response)