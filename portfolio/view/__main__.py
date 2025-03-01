from lib.auth0 import jwt
from lib.common import constants

def main(args):
    if jwt.verify_token('Token'):
        print(args)
        return {'status': 200, 'body': { 'message': f'Called the {constants.portfolio_label} view function'} }
    else:
        return {'status': 401, 'body': { 'message': 'Unauthorized'}}


if __name__ == '__main__':
    print(main({}))
