from lib.auth0 import jwt
from lib.common import constants

def main(args):
    if jwt.verify_token('Token'):
        print(args)
        return {'body': { 'message': f'Called the {constants.portfolio_label} search function'}, 'status': 200 }
    else:
        return {'body': { 'message': 'Unauthorized'}, 'status': 401}


if __name__ == '__main__':
    print(main({}))
