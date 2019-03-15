import argparse
import time

def main(args):
    import json

    # from message import messenger
    #
    # messenger_flag = messenger.Messenger('flag')
    # messenger_option = messenger.Messenger('option')
    # messenger_argument = messenger.Messenger('argument')
    #
    # messenger_flag.message([str(args.f)])
    # messenger_option.message([str(args.o)])
    # messenger_argument.message([str(args.argument)])

    time.sleep(10)

    print(str(args.argument))
    print(str(args.f))
    print(str(args.o))

    # testing = 1
    # test_val_json = {
    #     'flag': args.f,
    #     'option': args.o,
    #     'argument': args.argument
    # }
    # with open('/Users/elliottevers/Documents/Documents - Elliott’s MacBook Pro/git-repos.nosync/music/sandbox/data.json', 'w') as outfile:
    #     json.dump(test_val_json, outfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run Python from Max')

    parser.add_argument('argument', help='help for argument')
    #
    parser.add_argument('--o', help='help for option')
    # #
    parser.add_argument('-f', help='help for flag', action='store_true')
    #
    args = parser.parse_args()
    #
    main(args)

