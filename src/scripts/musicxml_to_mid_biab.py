import sys
sys.path.insert(0, '/Users/elliottevers/Documents/git-repos.nosync/tk_music_py/src')
import argparse
from music21 import converter, harmony, chord, stream, duration
from utils import utils


def main(args):
    file_input = utils.parse_arg(args.file_input)

    file_output = utils.parse_arg(args.file_output)

    score = converter.parse(file_input)

    part_new = stream.Part()

    for p in score:
        if isinstance(p, stream.Part):
            for m in p:
                if isinstance(m, stream.Measure):
                    chord_symbols = [c for c in m if isinstance(c, harmony.ChordSymbol)]

                    for sym in chord_symbols:
                        chord_new = chord.Chord(
                            [p.midi for p in sym.pitches],
                            duration=duration.Duration(4/len(chord_symbols))
                        )

                        part_new.append(chord_new)

    part_new.write('midi', fp=file_output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Band in a Box MusicXML to MIDI')

    parser.add_argument('--file_input', help='BIAB music xml file')

    parser.add_argument('--file_output', help='destination midi file')

    args = parser.parse_args()

    main(args)
