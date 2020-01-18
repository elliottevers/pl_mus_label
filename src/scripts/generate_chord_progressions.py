import sys
sys.path.insert(0, '/Users/elliottevers/Documents/git-repos.nosync/tk_music_py/src')

import random, argparse
from music21 import scale, pitch, key, stream, chord, roman, duration, note
from utils import utils
from message import messenger as mes

# import pydevd
# pydevd.settrace('localhost', port=8008, stdoutToServer=True, stderrToServer=True)

roman_numerals = {
    1: 'I',
    2: 'ii',
    3: 'iii',
    4: 'IV',
    5: 'V',
    6: 'vi'
}

graph = {
    1: [2, 4, 5],
    2: [3, 5],
    3: [2, 4, 6],
    4: [1, 3, 5],
    5: [1, 2, 6],
    6: [2, 4, 5]
}

beats_buffer = 2  # half the duration of a chord

# generate circle of fifths
edgeList = ['P5'] * 6 + ['d6'] + ['P5'] * 5
net5ths = scale.intervalNetwork.IntervalNetwork()
net5ths.fillBiDirectedEdges(edgeList)
circle_of_fifths = net5ths.realizePitch(pitch.Pitch('C1'))

SCALAR = 'scalar'
FIFTHS = 'fifths'

note_crash_cymbal = 'C#3'


def main():
    messenger = mes.Messenger()

    mode = utils.parse_arg(args.mode)

    part_predict = stream.Part()

    part_gt = stream.Part()

    part_segment = stream.Part()

    if mode == SCALAR:
        # generate random scale from circle of fifths
        struct_tones = scale.MajorScale(circle_of_fifths[random.choice(list(range(0, len(circle_of_fifths) - 1)))]).pitches[:-1]
    elif mode == FIFTHS:
        struct_tones = circle_of_fifths[:-1]
    else:
        raise('mode not supported')

    index_tones_current = random.choice(list(range(0, len(struct_tones) - 1)))

    tone_current = struct_tones[index_tones_current]

    key_current = key.Key(tone_current)

    length_beats = 4 * 8 * 2

    for i_measure in range(0, length_beats):
        if i_measure % 4 == 0:
            degree_current = 1

            part_segment.append(
                [
                    note.Note(
                        note_crash_cymbal,
                        duration=duration.Duration(4 * 2)
                    ),
                    note.Rest(
                        duration=duration.Duration(4 * 2)
                    )
                ]
            )

        elif i_measure % 4 == 3:
            key_next_diff = 1 if random.uniform(0, 1) > .5 else -1
            index_tones_current = (index_tones_current + key_next_diff) % len(struct_tones)
            tone_current = struct_tones[index_tones_current]
            key_current = key.Key(tone_current)
            degree_current = 5
        else:
            degree_current = random.choice(graph[degree_current])

        arp = chord.Chord(
            roman.RomanNumeral(roman_numerals[degree_current], key_current),
            duration=duration.Duration(4)
        ).closedPosition(forceOctave=3)

        n = [
            note.Rest(duration=duration.Duration(beats_buffer)),
            note.Note(
                arp.pitches[0],
                duration=duration.Duration(beats_buffer/3),
            ),
            note.Note(
                arp.pitches[1],
                duration=duration.Duration(beats_buffer/3),
            ),
            note.Note(
                arp.pitches[2],
                duration=duration.Duration(beats_buffer/3),
            )
        ]

        c = chord.Chord(
            roman.RomanNumeral(roman_numerals[degree_current], key_current),
            duration=duration.Duration(4)
        ).closedPosition(forceOctave=4)

        if i_measure < length_beats - 2:
            part_predict.append(
                c
            )
            part_gt.append(
                n
            )

    part_predict.write('midi', fp='/Users/elliottevers/Downloads/predict.mid')
    part_gt.write('midi', fp='/Users/elliottevers/Downloads/gt.mid')
    part_segment.write('midi', fp='/Users/elliottevers/Downloads/segment.mid')

    messenger.message(['done', 'bang'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Modulation Chord Progressions')

    parser.add_argument('--mode', help='scalar or fifths')

    args = parser.parse_args()

    main()
