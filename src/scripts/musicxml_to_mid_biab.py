import sys
sys.path.insert(0, '/Users/elliottevers/Documents/git-repos.nosync/tk_music_py/src')
import argparse
from music21 import converter, harmony, chord, note, stream, duration
from utils import utils
from message import messenger as mes
from postprocess import music_xml as postp_mxl


num_measures_lead_in = 2


def main(args):
    messenger = mes.Messenger()

    file_input = utils.parse_arg(args.file_input)

    file_output = utils.parse_arg(args.file_output)

    name_part = utils.parse_arg(args.name_part)

    score = converter.parse(file_input)

    part_new = stream.Part()

    for p in score:
        if isinstance(p, stream.Part):
            for i in range(num_measures_lead_in + 1, p.measure(-1).measureNumber + 1):
                m = p.measure(i)

                chord_symbols = [c for c in m if isinstance(c, harmony.ChordSymbol)]

                if len(chord_symbols) == 0:
                    if name_part == 'chord':
                        chord_new = chord.Chord(
                            [p.midi for p in chord_sym_last.pitches],  # NB: we want to fail in this case
                            duration=duration.Duration(4)
                        )
                        part_new.append(chord_new)
                        chord_sym_last = chord_new
                    elif name_part == 'root':
                        note_new = chord.Chord(
                            [[p.midi for p in chord_sym_last.pitches][0]],  # NB: we want to fail in this case
                            duration=duration.Duration(4)
                        )
                        part_new.append(note_new)
                        chord_sym_last = chord.Chord(
                            [p.midi for p in chord_sym_last.pitches],
                            duration=duration.Duration(4)
                        )
                    else:
                        raise Exception('cannot parse name_part from BIAB musicxml')
                else:
                    for sym in chord_symbols:
                        if name_part == 'chord':
                            chord_new = chord.Chord(
                                [p.midi for p in sym.pitches],
                                duration=duration.Duration(4/len(chord_symbols))
                            )
                            part_new.append(chord_new)
                            chord_sym_last = chord_new
                        elif name_part == 'root':
                            note_new = note.Note(
                                [p.midi for p in sym.pitches][0],
                                duration=duration.Duration(4/len(chord_symbols))
                            )

                            part_new.append(note_new)
                            chord_sym_last = chord.Chord(
                                [p.midi for p in sym.pitches],
                                duration=duration.Duration(4/len(chord_symbols))
                            )
                        else:
                            raise Exception('cannot parse name_part from BIAB musicxml')

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

    args = parser.parse_args()

    main(args)
