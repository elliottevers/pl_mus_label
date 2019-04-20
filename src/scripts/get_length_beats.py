from message import messenger as mes
import argparse
from utils import utils


def main(args):

    messenger = mes.Messenger()

    (
        _,
        _,
        _,
        _,
        length_beats,
        _,
        _
    ) = utils.get_grid_beats(
        use_warped=utils.b_use_warped()
    )

    messenger.message(['length_beats', str(length_beats)])

    messenger.message(['done', 'bang'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get length of training data in beats')

    args = parser.parse_args()

    main(args)
