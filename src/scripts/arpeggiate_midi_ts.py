import sys

sys.path.insert(0, '/Users/elliottevers/Documents/git-repos.nosync/tk_music_py/src')
from utils.utils import get_object_potentially_callable
from mido import Message, MidiFile, MidiTrack
import argparse
from music21 import chord
from utils import utils
from message import messenger as mes

import pytube


def main(args):

    # video to sync midi to

    url = 'https://www.youtube.com/watch?v=dO1rMeYnOmM'

    dir_download = '/Users/elliottevers/Downloads/'

    pytube.YouTube(url).streams.filter(only_audio=True).first().download(dir_download)

    exit(0)

    # midi timeseries

    # messenger = mes.Messenger()

    # filepath_input = utils.parse_arg(args.file_input)

    # filepath_output = utils.parse_arg(args.file_output)

    filepath_input = utils.parse_arg(dir_download + 'Chordify_Jim-Croce-Time-in-a-bottle-1973_Time_Aligned_136_BPM.mid')

    filepath_output = utils.parse_arg(dir_download + 'buffered_arpeggio.mid')

    # NB: relying on preservation of insertion order
    ts_note_on = {}
    ts_note_off = {}

    file_input = MidiFile(filepath_input)

    # TODO:
    # create MIDI timeseries (s -> List[Note])
    # for groups of notes at given time, determine the chord with music21
    # write either root, third, or fifth to separate ts
    # create new midi file
    time_current = 0
    for msg in file_input.tracks[0]:
            time_current = time_current + msg.time
            if msg.type == 'note_on':
                ts_note_on[time_current] = ts_note_on.get(time_current, []) + [msg.note]
            if msg.type == 'note_off':
                ts_note_off[time_current] = ts_note_off.get(time_current, []) + [msg.note]

    time_current = 0
    for msg in file_input.tracks[1]:
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
    pitch21_last = chord.Chord(list(ts_note_on.values())[0]).root()

    for time, pitches in ts_note_on.items():

        duration = time - time_last

        c = chord.Chord(pitches).closedPosition(forceOctave=4)

        tones = [x for x in [c.root(), c.third, c.fifth] if x]

        for tone in tones:
            track.append(Message('note_off', note=pitch21_last.midi, velocity=0, time=int(duration/len(tones))))
            track.append(Message('note_on', note=tone.midi, velocity=90, time=0))
            pitch21_last = tone
            time_last = time

    obj = chord.Chord(list(ts_note_off.values())[-1]).root()

    note_off_final_midi = get_object_potentially_callable(obj).midi

    track.append(
        Message(
            'note_off',
            note=note_off_final_midi,
            velocity=0,
            time=list(zip(list(ts_note_on), list(ts_note_off)))[-1][1] - list(zip(list(ts_note_on), list(ts_note_off)))[-1][0]
        )
    )

    file_output.save(filepath_output)

    # messenger.message(['done', 'bang'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Arpeggiate Chordify MIDI, with buffer')

    parser.add_argument('--file_input', help='Chordify MIDI file')

    parser.add_argument('--file_output', help='extracted part')

    parser.add_argument('--index_part_extract', help='1, 3, 5 - root, third, fifth')

    args = parser.parse_args()

    main(args)
