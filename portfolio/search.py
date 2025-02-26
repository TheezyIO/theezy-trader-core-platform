from common import constants

def main(args):
    print(args)
    return {'status': 200, 'message': f'Called the {constants.portfolio_label} search function'}
