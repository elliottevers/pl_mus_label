from information_retrieval import extraction as ir
from filter import seconds as s_filt
from preprocess import vamp as prep_vamp
from message import messenger as mes
from filter import hertz as filt_hz, midi as filt_mid
from utils import utils
from convert import max as conv_max
import argparse
from typing import Dict


def filter(params, type_substrate):
    if type_substrate == 'hz':
        df_filtered = filt_hz.apply_filters(
            params
        )
    elif type_substrate == 'mid':
        df_filtered = filt_mid.apply_filters(
            params
        )
    else:
        raise 'substrate type ' + type_substrate + ' not supported'

    return df_filtered


def main(args):
    messenger = mes.Messenger()

    messenger.message(['running'])

    filter_map: Dict[int, Dict[str, float]] = args.filter_map

    type_substrate = args.type_substrate

    for i, params in filter_map:
        df_filtered = filt_hz.apply_filters(
            params
        )

        conv_max.to_coll(
            df_filtered,
            filepath=utils.get_path_melody_filtered(
                i,
                type_substrate=type_substrate
            )
        )

    messenger.message(['done'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Apply filters to timeseries of extracted melody')

    parser.add_argument('filter_map', help='filters to apply')

    parser.add_argument('type_substrate', help='hertz or midi')

    args = parser.parse_args()

    main(args)
