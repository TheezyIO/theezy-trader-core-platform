from lib.common import constants

def main(args):
    print(args)
    return {'status': 200, 'message': f'Called the {constants.portfolio_label} search function'}


if __name__ == '__main__':
    print(main({}))
