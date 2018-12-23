import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage
from music21 import stream as stream21, note as note21, pitch as pitch21, duration as duration21
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import convert.series_to_mid as series2mid
import music21
import os
import importlib

sns.set(style="darkgrid")

# importlib.import_module(os.path.dirname(os.path.realpath(mido.__file__)) + '/midifiles/midifiles.py')

# mido, midifiles.py

DEFAULT_TEMPO = 500000

filename_input = '/Users/elliottevers/Downloads/ella_dream_vocals_2.mid'

filename_output = '/Users/elliottevers/Downloads/output_midi_to_ticks_timeseries.mid'

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

stream = stream21.Stream()

thing = []

for msg in file:

    if msg.type == 'note_on':
        # assert len(thing) == 0  # monophonic

        ticks_since_onset_last = int(round(mido.second2tick(msg.time, ticks_per_beat, mido.bpm2tempo(bpm))))
        track.append(Message('note_on', note=msg.note, velocity=msg.velocity, time=ticks_since_onset_last))
        # quarter note in ticks - ticks_since_onset_last/ticks_per_beat
        # duration = duration21.Duration()
        # duration.quarterLength = ticks_since_onset_last/ticks_per_beat

        pitch = pitch21.Pitch()
        pitch.midi = msg.note

        note = note21.Note()
        # note.duration = duration
        note.pitch = pitch

        # stream.append(note)
        thing.append(note)

        for tick_empty in range(ticks_since_onset_last):
            iter_tick += 1
            ticks.append(tick_last + tick_empty)
            notes_midi.append(None)

    if msg.type == 'note_off':
        # assert len(thing) == 1  # monophonic

        ticks_since_onset_last = int(round(mido.second2tick(msg.time, ticks_per_beat, mido.bpm2tempo(bpm))))
        track.append(Message('note_off', note=msg.note, velocity=msg.velocity, time=ticks_since_onset_last))

        duration = duration21.Duration()
        duration.quarterLength = ticks_since_onset_last / ticks_per_beat

        note = thing.pop()

        note.duration = duration

        stream.append(note)

        # pitch = pitch21.Pitch()
        # pitch.midi = msg.note
        #
        # note = note21.Note()
        # note.duration = duration
        # note.pitch = pitch
        #
        # stream.append(note)

        for tick in range(ticks_since_onset_last):
            iter_tick += 1
            ticks.append(tick_last + tick)
            notes_midi.append(msg.note)

    tick_last = iter_tick


# TODO: we're trying to convert to music21 object here - this also might be the key to making monophonic midi file

df = pd.Series(
    notes_midi,
    index=np.array(ticks)
)


mid2 = MidiFile(ticks_per_beat=ticks_per_beat)

track2 = MidiTrack()

mid2.tracks.append(
    series2mid.timeseries_ticks_to_mid(
        df,
        track2,
        90
    )
)

lim = int(round(len(df.index)/4))

sns.relplot(kind="line", data=df[1:lim])


plt.show()


# df.plot()

# stream.plot()
mid2.save(filename_output)