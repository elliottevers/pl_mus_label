import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage
import os
import importlib

# importlib.import_module(os.path.dirname(os.path.realpath(mido.__file__)) + '/midifiles/midifiles.py')

# mido, midifiles.py

DEFAULT_TEMPO = 500000

filename_input = '/Users/elliottevers/Downloads/ella_dream_vocals_2.mid'

filename_output = '/Users/elliottevers/Downloads/monophonify.mid'

program_change = 22  # harmonica

file = MidiFile(filename_input)

ticks_per_beat = file.ticks_per_beat

ppq = ticks_per_beat

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

note_on = False

note_sounding = None

acc_time = 0

for msg in file:

    if msg.type == 'note_on' and not note_on:
        message = Message(
            'note_on',
            note=msg.note,
            velocity=msg.velocity,
            time=int(round(mido.second2tick(
                acc_time + msg.time,
                ticks_per_beat=ticks_per_beat,
                tempo=DEFAULT_TEMPO
            )))
        )
        track.append(message)
        note_sounding = msg.note
        note_on = True
        acc_time = 0
    if msg.type == 'note_on' and note_on:  # if two simultaneous, turn first off
        message_off = Message(
            'note_off',
            note=note_sounding,
            velocity=0,
            time=int(round(mido.second2tick(
                acc_time + msg.time,
                ticks_per_beat=ticks_per_beat,
                tempo=DEFAULT_TEMPO
            )))
        )
        message_on = Message(
            'note_on',
            note=msg.note,
            velocity=msg.velocity,
            time=0
        )
        track.append(message_off)
        track.append(message_on)
        note_sounding = msg.note
        note_on = True
        acc_time = 0
    elif msg.type == 'note_off' and not note_on:
        acc_time += msg.time
        # print('happened')
    elif msg.type == 'note_off' and note_on:
        message_off = Message(
            'note_off',
            note=note_sounding,
            velocity=0,
            time=int(round(mido.second2tick(
                msg.time,
                ticks_per_beat=ticks_per_beat,
                tempo=DEFAULT_TEMPO
            )))
        )
        track.append(message_off)
        note_on = False
        note_sounding = None
        acc_time = 0

mid.save(filename_output)