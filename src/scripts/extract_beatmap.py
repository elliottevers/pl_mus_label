from information_retrieval import extraction as ir
from message import messenger as mes
import argparse


def main(args):
    messenger = mes.Messenger()

    messenger.message(['running'])

    filename_wav = args.filename

    ir.extract_beats(
        filename_wav
    )

    messenger.message(['done'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Estimate Beats')

    parser.add_argument('filepath', help='audio file from which to extract beat estimates')

    args = parser.parse_args()

    main(args)
