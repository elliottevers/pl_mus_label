import sys
sys.path.insert(0, '/Users/elliottevers/Documents/git-repos.nosync/tk_music_py/src')
from message import messenger as mes
import argparse
from convert import max as conv_max
import music21
from utils import utils
# import string
# from collections import OrderedDict
# from pyts.quantization import SAX, SFA, MCB


def main(args):

    note_midi_lower = int(utils.parse_arg(args.note_midi_lower))
    note_midi_upper = int(utils.parse_arg(args.note_midi_upper))

    chromatic_scale = music21.scale.ChromaticScale(
        music21.pitch.Pitch(midi=note_midi_lower)
    )

    # pitches = [
    #     str(p)
    #     for p
    #     in chromatic_scale.getPitches(
    #         music21.pitch.Pitch(midi=note_midi_lower),
    #         music21.pitch.Pitch(midi=note_midi_upper)
    #     )
    # ]
    #
    # pitches.insert(0, 0)
    #
    # alphabet_map = dict()
    #
    # for tuple in list(set(zip(list(string.ascii_lowercase), pitches))):
    #     alphabet_map[tuple[0]] = tuple[1]

    # this will put the letter 'l' at the front
    # alphabet_map_sorted = utils.rotate_items(OrderedDict(sorted(alphabet_map.items())), 11)
    #
    # n_bins = note_midi_upper - note_midi_lower + 2

    df = conv_max.from_coll(
        filename=conv_max.file_ts_coll
    )

    frequencies_hz = [
        p.frequency
        for p
        in chromatic_scale.getPitches(
            music21.pitch.Pitch(midi=note_midi_lower - 1),
            music21.pitch.Pitch(midi=note_midi_upper + 1)
        )
    ]

    pitches = chromatic_scale.getPitches(
        music21.pitch.Pitch(midi=note_midi_lower),
        music21.pitch.Pitch(midi=note_midi_upper)
    )

    df['signal_discretized'] = df['signal'] * 0

    for pitch in pitches:
        range_hz = (
            (music21.pitch.Pitch(midi=pitch.midi - 1).frequency + pitch.frequency)/2,
            (music21.pitch.Pitch(midi=pitch.midi + 1).frequency + pitch.frequency)/2
        )
        df['signal_discretized'][(range_hz[0] <= df['signal']) & (range_hz[1] >= df['signal'])] = pitch.frequency

    threshold_lower = (frequencies_hz[0] + frequencies_hz[1])/2

    threshold_upper = (frequencies_hz[-2] + frequencies_hz[-1])/2

    df['signal_discretized'][df['signal'] < threshold_lower] = 0

    df['signal_discretized'][df['signal'] > threshold_upper] = 0

    # sax = SAX(
    #     n_bins=n_bins,
    #     quantiles='empirical'
    # )

    # sfa = SFA(
    #     n_bins=n_bins,
    #     quantiles='empirical'
    # )

    # mcb = MCB(
    #     n_bins=n_bins,
    #     quantiles='gaussian'
    # )

    # def lookup_frequency(letter: str) -> int:
    #     return music21.pitch.Pitch(alphabet_map_sorted[letter]).frequency

    # df['signal_discretized'] = sax.fit_transform(df['signal'].values.reshape((1, len(df.index))))[0]
    # df['signal_discretized'] = sfa.fit_transform(df['signal'].values.reshape((1, len(df.index))))

    # df['signal_discretized'] = df['signal_discretized'].apply(lookup_frequency)

    conv_max.to_coll(
        df[['pos', 'signal_discretized']].rename(columns={'signal_discretized': 'signal'}),
        filename=conv_max.file_ts_coll_discrete
    )

    messenger = mes.Messenger()

    messenger.message(['done', 'bang'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Discretize filtered Hertz melody')

    parser.add_argument('--note_midi_lower', help='lower threshold')

    parser.add_argument('--note_midi_upper', help='upper threshold')

    args = parser.parse_args()

    main(args)
