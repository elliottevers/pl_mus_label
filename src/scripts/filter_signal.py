from information_retrieval import extraction as ir
# from filter import seconds as s_filt
from preprocess import vamp as prep_vamp
from message import messenger as mes
from utils import utils
from convert import max as conv_max
import argparse
from typing import Dict
import pandas as pd


def main(args):

    # filter_map: Dict[int, Dict[str, float]] = args.filter_map


    filter = 'medfilt'

    filter_map: Dict[int, Dict[str, float]] = {
        'kernel_size': [
            111,
            311,
            511
        ]
    }

    df_to_filter = conv_max.from_coll(
        filename=conv_max.file_ts_coll
    )

    params = filter_map

    from scipy import signal
    import numpy as np

    for name_argument, values in params.items():
        for i_value, value in enumerate(values):
            df_to_filter['signal_filtered'] = \
                pd.Series(
                    getattr(signal, filter)(df_to_filter['signal'].as_matrix().reshape(-1, ), **{name_argument: value}),
                    dtype=np.float
                )

    conv_max.to_coll(
        df_to_filter[['pos', 'signal_filtered']].rename(columns={'signal_filtered': 'signal'}),
        filename=conv_max.file_ts_coll
    )

    messenger = mes.Messenger()

    messenger.message(['done'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Apply filters to timeseries of extracted melody')

    # TODO: add filtering parameters

    # parser.add_argument('filter_map', help='filters to apply')

    args = parser.parse_args()

    main(args)
