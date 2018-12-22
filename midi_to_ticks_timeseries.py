import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage
import os
import importlib

# importlib.import_module(os.path.dirname(os.path.realpath(mido.__file__)) + '/midifiles/midifiles.py')

# mido, midifiles.py

DEFAULT_TEMPO = 500000

filename_input = '/Users/elliottevers/Downloads/ella_dream_vocals_2.mid'

filename_output = '/Users/elliottevers/Downloads/correct_length.mid'

program_change = 22  # harmonica

file = MidiFile(filename_input)

ticks_per_beat = file.ticks_per_beat

mid = MidiFile(ticks_per_beat=ticks_per_beat)
track = MidiTrack()
mid.tracks.append(track)

track.append(
    Message(
        'program_change',
        program=program_change,
        time=0
    )
)

iter_tick = 0

tick_last = 0

ticks = []

notes_midi = []

bpm = mido.tempo2bpm(DEFAULT_TEMPO)

track.append(
    MetaMessage(
        'time_signature',
        time=0
    )
)

track.append(
    MetaMessage(
        'set_tempo',
        tempo=mido.bpm2tempo(bpm),
        time=0
    )
)

for msg in file:
    if msg.type == 'note_on':
        ticks_since_onset_last = int(round(mido.second2tick(msg.time, ticks_per_beat, mido.bpm2tempo(bpm))))
        track.append(Message('note_on', note=msg.note, velocity=msg.velocity, time=ticks_since_onset_last))
        for tick_empty in range(ticks_since_onset_last):
            iter_tick += 1
            ticks.append(tick_last + tick_empty)
            notes_midi.append(None)

    if msg.type == 'note_off':
        ticks_since_onset_last = int(round(mido.second2tick(msg.time, ticks_per_beat, mido.bpm2tempo(bpm))))
        track.append(Message('note_off', note=msg.note, velocity=msg.velocity, time=ticks_since_onset_last))
        for tick in range(ticks_since_onset_last):
            iter_tick += 1
            ticks.append(tick_last + tick)

    tick_last = iter_tick


mid.save(filename_output)