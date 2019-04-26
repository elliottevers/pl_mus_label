import sys
sys.path.insert(0, '/Users/elliottevers/Documents/DocumentsSymlinked/git-repos.nosync/music/src')
from message import messenger as mes
import argparse
from utils import utils


def main(args):

    messenger = mes.Messenger()

    (
        s_beat_start,
        s_beat_end,
        tempo,
        beat_start,
        beat_end,
        length_beats,
        beatmap
    ) = utils.get_tuple_beats()

    messenger.message(['length_beats', str(length_beats)])

    messenger.message(['done', 'bang'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get length of training data in beats')

    args = parser.parse_args()

    main(args)
