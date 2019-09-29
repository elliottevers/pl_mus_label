import sys
sys.path.insert(0, '/Users/elliottevers/Documents/git-repos.nosync/tk_music_py/src')
from message import messenger as mes
import argparse


def main(args):
    b = args.b

    messenger = mes.Messenger()

    messenger.message([b])

    messenger.message(['done', 'bang'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Estimate Beats')

    parser.add_argument('--b', help='beat start marker in seconds')

    args = parser.parse_args()

    main(args)
