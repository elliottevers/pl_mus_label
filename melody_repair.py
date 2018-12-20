# plot the midi file

# HAS TO BE MONOPHONIC

from music21 import midi, converter, environment, tempo

# us = environment.UserSettings()
# us.create()
#
# for key in sorted(us.keys()):
#     print(key)

# us = environment.UserSettings()
# print(us.getSettingsPath())

# environment.set('musescoreDirectPNGPath', '/Applications/MuseScore 2.app/Contents/MacOS/mscore')


file_midi = midi.MidiFile()

file_midi.open(
    filename='/Users/elliottevers/Downloads/ella_dream_vocals.mid',
    attrib='rb'
)

# stream = midi.translate.midiFileToStream(
#     file_midi
# )

stream = converter.parse('/Users/elliottevers/Downloads/ella_dream_vocals.mid')

# stream.show('midi')

# stream.plot('histogram', 'pitch')

# stream.plot('histogram', 'duration')

# for note in stream:
#     for pitch in note.pitches:
#         print(pitch.midi)

# for note in stream.part.pitches:
#     print(note)

testing = 1

# stream.plot('pianoroll')


# TODO:
# plot parts of stream
# histogram to decide what value to initialize value of windowed average
# try starting with mean of entire score



# TODO: define window

notes_filtered = []

for part in stream:
    for note in part.notes:
        # stream.remove(note)
        notes_filtered.append(note)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="darkgrid")


# from seaborn import

len_window = 0  # int in ticks

len_series = 0  # int in ticks

# tick to currently sounding event mapping

series = pd.Series([])

# for tick in range(len_series - len_window):
#     window = series.between(tick, tick + len_window)
#     std = window.std()

# df = pd.DataFrame(
#     dict(
#         time=np.arange(500),
#         value=np.random.randn(500).cumsum()
#     )
# )

# tesing = dict(time=np.arange(500),value=np.random.randn(500).cumsum())

# g = sns.relplot(x="time", y="value", kind="line", data=df)
#
# g.fig.autofmt_xdate()
#
# plt.show()
# stream.parts[0].remove(notes_filtered)

# midi.translate.durationToMidi(part.duration) = 375552

# ticks = dict()

ticksPerQuarter = 1024  # default

notes = []


def get_note(ref_note):
    return notes[ref_note]


ticks = []
events_midi = []

for part in stream:
    duration_entire_ticks = midi.translate.durationToMidi(part.duration)
    for note in part.notes:
        notes.append(note)
        # bug in music21 - no object _quarterLengthNeedsUpdating
        offset_ticks = int(round(note.offset * ticksPerQuarter))
        duration_ticks = midi.translate.durationToMidi(note.duration)

        ref_note = len(notes) - 1
        for tick in range(duration_ticks - 1):
            ticks.append(offset_ticks + tick)
            events_midi.append(ref_note)
            # ticks[duration_offset + tick] = ref_note
        # print(note)


# len ticks == duration_entire_ticks




# stream.show()

testing = 1

# dict - tick -> midi event

# compute number of ticks for the stream

# ticks = things per quarter note

# data = dict(
#     time=ticks,
#     value=events_midi
# )

df = pd.DataFrame(
    dict(
        ticks=ticks,
        events=events_midi
    )
)

#
# data = sns.load_dataset("fmri")

sns.relplot(x="ticks", y="events", kind="line", ci="sd", data=df)

plt.show()


mf = midi.translate.streamToMidiFile(stream)

print(len(mf.tracks[0].events))

# stream.plot('histogram', 'duration')