from information_retrieval import extraction as ir
from filter import seconds as s_filt
from preprocess import vamp as prep_vamp
from message import messenger as mes
from filter import hertz as filt_hz
from utils import utils
from convert import max as conv_max
import argparse
from typing import Dict
from scipy.stats import norm
from pyts.quantization import SAX
import numpy as np


# TODO: the hardest thing here is:
# 1) filter the raw timeseries for values outside of chosen range of notes
# 2) discretize the ones left, keeping the index
# 3) merge back into the

def main(args):
    messenger = mes.Messenger()

    messenger.message(['running'])

    note_midi_lower = args.note_midi_lower

    note_midi_upper = args.note_midi_upper

    index_melody_hz_filtered_chosen = args.index_melody_hz_filtered_chosen

    n_bins = note_midi_upper - note_midi_lower

    df_melody_hz_filtered_chosen = conv_max.from_coll(
        filepath=utils.get_path_melody_hz_filtered(
            index_melody_hz_filtered_chosen
        )
    )

    df_within_user_defined_range = filt_hz.between(
        lower=note_midi_lower,
        upper=note_midi_upper,
        data=df_melody_hz_filtered_chosen
    )

    sax = SAX(
        n_bins=n_bins,
        quantiles='empirical'
    )

    # TODO: this might not be necessary once we refresh our understanding of SAX api

    data_melody = postp_vamp.to_data_melody(
        df_within_user_defined_range
    )

    n_samples, n_features = data_melody[1].shape, 1

    X = data_melody[1].reshape(1, data_melody[1].shape[0])

    X[X <= 0] = 0

    X_sax = sax.fit_transform(X)

    # bins = norm.ppf(np.linspace(0, 1, n_bins + 1)[1:-1])

    df_melody_discretized = postp_mid.to_df(
        X_sax
    )

    df_melody_mid_full = postp_mid.merge(
        df_melody_hz_filtered_chosen,
        df_melody_discretized
    )

    # df_melody_mid_diff = filt_mid.to_diff(
    #     df_melody_mid
    # )

    conv_max.to_coll(
        df_melody_mid_full,
        filepath=utils.FILE_MELODY_DISCRETIZED
    )

    messenger.message(['done'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Discretize filtered Hertz melody')

    parser.add_argument('index_melody_hz_filtered_chosen', help='which of the filtered timeseries to discretize')

    parser.add_argument('note_midi_lower', help='lower threshold')

    parser.add_argument('note_midi_upper', help='upper threshold')

    note_midi_lower = args.note_midi_lower

    note_midi_upper = args.note_midi_upper

    index_melody_hz_filtered_chosen = args.index_melody_hz_filtered_chosen

    args = parser.parse_args()

    main(args)
