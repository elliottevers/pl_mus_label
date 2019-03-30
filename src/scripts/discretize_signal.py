from message import messenger as mes
import argparse
from pyts.quantization import SAX, SFA, MCB
from convert import max as conv_max
import music21
import string
import math


def main(args):

    note_midi_lower = int(args.note_midi_lower.replace("\"", ''))

    note_midi_upper = int(args.note_midi_upper.replace("\"", ''))

    if note_midi_upper - note_midi_lower != 24:
        note_midi_upper = note_midi_lower + 24

    chromatic_scale = music21.scale.ChromaticScale(
        music21.pitch.Pitch(midi=note_midi_lower)
    )

    pitches = [
        str(p)
        for p
        in chromatic_scale.getPitches(
            music21.pitch.Pitch(midi=note_midi_lower),
            music21.pitch.Pitch(midi=note_midi_upper - 1)
        )
    ]

    # pitches.insert(0, -math.inf)
    pitches.insert(0, 0)

    # pitches.append(math.inf)
    pitches.append(0)

    alphabet_map = dict()

    for tuple in list(set(zip(list(string.ascii_lowercase), pitches))):
        alphabet_map[tuple[0]] = tuple[1]

    n_bins = note_midi_upper - note_midi_lower + 2

    df = conv_max.from_coll(
        filename=conv_max.file_ts_coll
    )

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
        return music21.pitch.Pitch(alphabet_map[letter]).frequency

    df['signal_discretized'] = sax.fit_transform(df['signal'].values.reshape((1, len(df.index))))[0]
    # df['signal_discretized'] = sfa.fit_transform(df['signal'].values.reshape((1, len(df.index))))

    df['signal_discretized'] = df['signal_discretized'].apply(lookup_frequency)

    conv_max.to_coll(
        df[['pos', 'signal_discretized']].rename(columns={'signal_discretized': 'signal'}),
        filename=conv_max.file_ts_coll_discrete
    )

    messenger = mes.Messenger()

    messenger.message(['done'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Discretize filtered Hertz melody')

    parser.add_argument('--note_midi_lower', help='lower threshold')

    parser.add_argument('--note_midi_upper', help='upper threshold')

    args = parser.parse_args()

    main(args)
