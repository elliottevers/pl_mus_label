from information_retrieval import extraction as ir
from filter import seconds as s_filt
from preprocess import vamp as prep_vamp
from message import messenger as mes
from filter import hertz as filt_hz
from utils import utils
from convert import max as conv_max
import argparse
from typing import Dict


def main(args):
    messenger = mes.Messenger()

    messenger.message(['running'])

    filter_map: Dict[int, Dict[str, float]] = args.filter_map

    for i, params in filter_map:
        df_hz_filtered = filt_hz.apply_filters(
            params
        )

        conv_max.to_coll(
            df_hz_filtered,
            filepath=utils.get_path_melody_hz_filtered(
                i
            )
        )

    messenger.message(['done'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Apply filters to hertz timeseries of extracted melody')

    parser.add_argument('filter_map', help='filters to apply')

    args = parser.parse_args()

    main(args)
