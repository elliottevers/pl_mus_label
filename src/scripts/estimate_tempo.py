import sys
sys.path.insert(0, '/Users/elliottevers/Documents/git-repos.nosync/music/src')
from information_retrieval import extraction as ir
import argparse
from message import messenger as mes


def main(args):
    tempo_estimate = ir.extract_tempo()

    messenger = mes.Messenger()

    messenger.message([str(tempo_estimate)])

    messenger.message(['done', 'bang'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Estimate Tempo')

    args = parser.parse_args()

    main(args)
