import sys
sys.path.insert(0, '/Users/elliottevers/Documents/git-repos.nosync/tk_music_py/src')
import argparse
from mido import Message, MidiFile, MidiTrack
from music21 import *


def get_object_potentially_callable(obj):
    return obj() if hasattr(obj, '__call__') else obj


def main(args):

    index_part_extract = 5

    index_part_to_interval = {
        1: 'root',
        3: 'third',
        5: 'fifth'
    }

    interval = index_part_to_interval[index_part_extract]

    # NB: relying on preservation of insertion order
    ts_note_on = {}
    ts_note_off = {}

    file_input = MidiFile('/Users/elliottevers/Downloads/tiny_dancer.mid')

    # TODO:
    # create MIDI timeseries (s -> List[Note])
    # for groups of notes at given time, determine the chord with music21
    # write either root, third, or fifth to separate ts
    # create new midi file
    time_current = 0
    for msg in file_input.tracks[1]:
        # for msg in track:
            time_current = time_current + msg.time
            if msg.type == 'note_on':
                ts_note_on[time_current] = ts_note_on.get(time_current, []) + [msg.note]
            if msg.type == 'note_off':
                ts_note_off[time_current] = ts_note_off.get(time_current, []) + [msg.note]

    time_current = 0
    for msg in file_input.tracks[2]:
        # for msg in track:
        time_current = time_current + msg.time
        if msg.type == 'note_on':
            ts_note_on[time_current] = ts_note_on.get(time_current, []) + [msg.note]
        if msg.type == 'note_off':
            ts_note_off[time_current] = ts_note_off.get(time_current, []) + [msg.note]

    file_output = MidiFile(ticks_per_beat=file_input.ticks_per_beat)
    track = MidiTrack()
    file_output.tracks.append(file_input.tracks[0])
    file_output.tracks.append(track)

    time_last = 0
    note21_last = get_object_potentially_callable(getattr(chord.Chord(list(ts_note_on.values())[0]), interval))

    for time, pitches in ts_note_on.items():
        chord_tone = get_object_potentially_callable(getattr(chord.Chord(pitches), interval))
        track.append(Message('note_off', note=note21_last.midi, velocity=0, time=(time - time_last)))
        track.append(Message('note_on', note=chord_tone.midi, velocity=90, time=0))
        note21_last = chord_tone
        time_last = time

    obj = getattr(chord.Chord(list(ts_note_off.values())[-1]), interval)

    note_off_final_midi = get_object_potentially_callable(obj).midi

    track.append(
        Message(
            'note_off',
            note=note_off_final_midi,
            velocity=0,
            time=list(zip(list(ts_note_on), list(ts_note_off)))[-1][1] - list(zip(list(ts_note_on), list(ts_note_off)))[-1][0]
        )
    )

    file_output.save('/Users/elliottevers/Downloads/tiny_dancer_output.mid')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Chordify')

    args = parser.parse_args()

    main(args)
