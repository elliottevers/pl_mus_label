import sys

sys.path.insert(0, '/Users/elliottevers/Documents/git-repos.nosync/tk_music_py/src')
import argparse
from music21 import converter, harmony, chord, note, stream, duration
from utils import utils
from message import messenger as mes
from postprocess import music_xml as postp_mxl

from utils.utils import get_object_potentially_callable


num_measures_lead_in = 2


def main(args):
    messenger = mes.Messenger()

    file_input = utils.parse_arg(args.file_input)

    file_output = utils.parse_arg(args.file_output)

    name_part = utils.parse_arg(args.name_part)

    score = converter.parse(file_input)

    part_new = stream.Part()

    index_part_extract = int(utils.parse_arg(args.index_part_extract))

    index_part_to_interval = {
        1: 'root',
        3: 'third',
        5: 'fifth'
    }

    interval = index_part_to_interval[index_part_extract]

    def process_chord_symbol(chord_sym, num_chord_symbols):
        dividend = num_chord_symbols if num_chord_symbols > 0 else 1

        if name_part == 'chord':
            chord_new = chord.Chord(
                [p.midi for p in chord_sym.pitches],  # NB: we want to fail in this case
                duration=duration.Duration(4 / dividend)
            )
            to_append = chord_new
            chord_sym_last = chord_new
        elif name_part == 'chord_tone':
            obj = getattr(chord_sym, interval)

            note_new = note.Note(
                get_object_potentially_callable(obj),
                duration=duration.Duration(4 / dividend)
            )
            to_append = note_new
            chord_sym_last = chord.Chord(
                [p.midi for p in chord_sym.pitches],
                duration=duration.Duration(4 / dividend)
            )
        else:
            raise Exception('cannot parse name_part from BIAB musicxml')

        return to_append, chord_sym_last

    for p in score:
        if isinstance(p, stream.Part):
            for i in range(num_measures_lead_in + 1, p.measure(-1).measureNumber + 1):
                m = p.measure(i)

                chord_symbols = [c for c in m if isinstance(c, harmony.ChordSymbol)]

                if len(chord_symbols) == 0:  # chord_sym_last should be defined here
                    to_append, chord_sym_last = process_chord_symbol(
                        chord_sym=chord_sym_last,
                        num_chord_symbols=0
                    )
                    part_new.append(to_append)
                else:
                    for sym in chord_symbols:
                        to_append, chord_sym_last = process_chord_symbol(
                            chord_sym=sym,
                            num_chord_symbols=len(chord_symbols)
                        )
                        part_new.append(to_append)

    if name_part == 'chord':
        part_new = postp_mxl.force_texture(
            part_new,
            num_voices=4
        )

    part_new.write('midi', fp=file_output)

    messenger.message(['done', 'bang'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Band in a Box MusicXML to MIDI')

    parser.add_argument('--file_input', help='BIAB music xml file')

    parser.add_argument('--file_output', help='destination midi file')

    parser.add_argument('--name_part', help='root or chord')

    parser.add_argument('--index_part_extract', help='1, 3, 5 - root, third, fifth')

    args = parser.parse_args()

    main(args)
