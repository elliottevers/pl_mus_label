from information_retrieval import extraction as ir
from preprocess import vamp as prep_vamp
from message import messenger as mes
from utils import utils
from convert import max as conv_max
import argparse
from typing import Dict
from scipy.stats import norm
from pyts.quantization import SAX, SFA, MCB
import numpy as np
from convert import max as conv_max
import pandas as pd
import music21


def main(args):

    # note_midi_lower = args.note_midi_lower
    #
    # note_midi_upper = args.note_midi_upper
    #
    # n_bins = note_midi_upper - note_midi_lower

    n_bins = 6

    df = conv_max.from_coll(
        filename=conv_max.file_ts_coll
    )

    # TODO: set all values that aren't in range to 0

    # TODO: dynamically create alphabet map

    # df_within_user_defined_range = filt_hz.between(
    #     lower=note_midi_lower,
    #     upper=note_midi_upper
    # )

    sax = SAX(
        n_bins=n_bins,
        quantiles='empirical'
    )

    # sfa = SFA(
    #     n_bins=n_bins,
    #     quantiles='empirical'
    # )

    # mcb = MCB(
    #     n_bins=n_bins,
    #     quantiles='gaussian'
    # )

    def lookup_frequency(letter: str) -> int:
        alphabet_map = {
            'a': 'C3',
            'b': 'D-3',
            'c': 'D3',
            'd': 'E-3',
            'e': 'E3',
            'f': 'F3',
            'g': 'G-3',
            'h': 'G3',
            'i': 'A-3',
            'j': 'A3',
            'k': 'A#3',
            'l': 'B3',
            'm': 'C4',
            'n': 'C#4',
            'o': 'D4',
            'p': 'D#4',
            'q': 'E4',
            'r': 'F4',
            's': 'F#4',
            't': 'G4',
            'u': 'G#4',
            'v': 'A4',
            'w': 'A#4',
            'x': 'B4',
            'y': 'C5',
            'z': 'C#5'
        }

        return music21.pitch.Pitch(alphabet_map[letter]).frequency

    # df['signal_discretized'] = sfa.fit_transform(df['signal'].values.reshape((1, len(df.index))))[0]
    df['signal_discretized'] = sfa.fit_transform(df['signal'].values.reshape((1, len(df.index))))

    df['signal_discretized'] = df['signal_discretized'].apply(lookup_frequency)

    conv_max.to_coll(
        df[['pos', 'signal_discretized']].rename(columns={'signal_discretized': 'signal'}),
        # filename=conv_max.file_ts_coll
        filename='/Users/elliottevers/Documents/DocumentsSymlinked/git-repos.nosync/tk_music_projects/ts_hz_discretized.txt'
    )

    messenger = mes.Messenger()

    messenger.message(['done'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Discretize filtered Hertz melody')

    # TODO: add discretization parameters

    # parser.add_argument('index_melody_hz_filtered_chosen', help='which of the filtered timeseries to discretize')
    #
    # parser.add_argument('note_midi_lower', help='lower threshold')
    #
    # parser.add_argument('note_midi_upper', help='upper threshold')

    args = parser.parse_args()

    main(args)
