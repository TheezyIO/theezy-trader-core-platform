from lib.common import constants

def main(args):
    print(args)
    if args.get('checkFile'):
        try:
            with open('test.txt', 'r') as txt_file:
                print('Found file')
                print(txt_file.read())
        except FileNotFoundError as e:
            print('Did not find the file')

    return {'status': 200, 'message': f'Called the {constants.portfolio_label} search function'}


if __name__ == '__main__':
    print(main({}))
