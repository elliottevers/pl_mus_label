import sys

sys.path.insert(0, '/Users/elliottevers/Documents/git-repos.nosync/tk_music_py/src')
from utils.utils import get_object_potentially_callable
from mido import Message, MidiFile, MidiTrack
import argparse
from music21 import chord
from utils import utils
from message import messenger as mes

import pytube

ratio_buffer = .5


def main(args):

    # video to sync midi to

    url = 'https://www.youtube.com/watch?v=2PTEqZURh4o'

    dir_download = '/Users/elliottevers/Downloads/'

    # pytube.YouTube(url).streams.filter(only_audio=True).first().download(dir_download)

    # exit(0)

    # midi timeseries

    # messenger = mes.Messenger()

    # filepath_input = utils.parse_arg(args.file_input)

    # filepath_output = utils.parse_arg(args.file_output)

    filepath_input = utils.parse_arg(dir_download + 'Chordify_Lyin-Eyes-2018-Remaster_Time_Aligned_130_BPM.mid')

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

    note_buffer = 48  # pitch21_last.midi

    chords = list(ts_note_on.items())

    for i, (time, pitches) in enumerate(chords[:-1]):

        duration = chords[i + 1][0] - time

        c = chord.Chord(pitches).closedPosition(forceOctave=4)

        tones_chord = c.pitches  # [c.root()]

        len_buffer = ratio_buffer * duration
        len_audible = (1 - ratio_buffer) * (duration / len(tones_chord))

        # silent (buffer)
        track.append(Message('note_on', note=note_buffer, velocity=0, time=0))
        track.append(Message('note_off', note=note_buffer, velocity=0, time=int(len_buffer)))

        for tone in tones_chord:
            # audible
            track.append(Message('note_on', note=tone.midi, velocity=90, time=0))
            track.append(Message('note_off', note=tone.midi, velocity=0, time=int(len_audible)))

    # TODO: add final chord

    file_output.save(filepath_output)

    # messenger.message(['done', 'bang'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Arpeggiate Chordify MIDI, with buffer')

    parser.add_argument('--file_input', help='Chordify MIDI file')

    parser.add_argument('--file_output', help='extracted part')

    parser.add_argument('--index_part_extract', help='1, 3, 5 - root, third, fifth')

    args = parser.parse_args()

    main(args)
