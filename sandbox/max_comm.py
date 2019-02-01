import argparse
import json


def main(args):
    print('flag\n')
    print(str(args.f) + '\n')
    print('option\n')
    print(args.o + '\n')
    print('argument\n')
    print(args.argument + '\n')

    test_val_json = {
        'flag': args.f,
        'option': args.o,
        'argument': args.argument
    }
    with open('/Users/elliottevers/Documents/Documents - Elliott’s MacBook Pro/git-repos.nosync/music/sandbox/data.json', 'w') as outfile:
        json.dump(test_val_json, outfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run Python from Max')

    parser.add_argument('argument', help='help for argument')

    parser.add_argument('--o', help='help for option')

    parser.add_argument('-f', help='help for flag', action='store_true')

    args = parser.parse_args()

    main(args)
