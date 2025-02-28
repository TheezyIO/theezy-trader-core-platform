from lib.common import constants

def main(args):
    print(args)
    return {'body': { 'message': f'Called the {constants.portfolio_label} search function'}, 'status': 200 }


if __name__ == '__main__':
    print(main({}))
