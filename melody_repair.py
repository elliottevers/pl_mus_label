# plot the midi file

# HAS TO BE MONOPHONIC

from music21 import midi, converter, environment, tempo
from music21 import note as note21, stream as stream21
from mido import MidiFile
import mido

# us = environment.UserSettings()
# us.create()
#
# for key in sorted(us.keys()):
#     print(key)

# us = environment.UserSettings()
# print(us.getSettingsPath())

# environment.set('musescoreDirectPNGPath', '/Applications/MuseScore 2.app/Contents/MacOS/mscore')

# TODO: check delta time of example for midiEventsToNote

# TODO: can we 1) create another stream 2) take notes out of first 3) add them to second and create midify the stream and have it sound the same as first?


stream_test = stream21.Stream()


# stream = converter.parse('/Users/elliottevers/Downloads/monophonic.mid')
#
# stream.show('midi')

from mido import Message, MidiFile, MidiTrack

mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

track.append(Message('program_change', program=12, time=0))

for msg in MidiFile('/Users/elliottevers/Downloads/monophonic.mid'):
    if msg.type == 'note_on':
        time_ticks = int(round(mido.second2tick(msg.time, 96, 120)))
        track.append(Message('note_on', note=msg.note, velocity=msg.velocity, time=time_ticks))

    if msg.type == 'note_off':
        time_ticks = int(round(mido.second2tick(msg.time, 96, 120)))
        track.append(Message('note_off', note=msg.note, velocity=msg.velocity, time=time_ticks))


mid.save('/Users/elliottevers/Downloads/yolo.mid')

# mid.save('/Users/elliottevers/Downloads/monophonic_mido.mid')

exit(0)

mt = midi.MidiTrack(1)

dt1 = midi.DeltaTime(mt)
dt1.time = 1024 * 2 * 2

me1 = midi.MidiEvent(mt)
me1.type = 'NOTE_ON'
me1.pitch = 45
me1.velocity = 94

dt2 = midi.DeltaTime(mt)
dt2.time = 1024 * 2 * 2 * 2 * 2

me2 = midi.MidiEvent(mt)
me2.type = 'NOTE_ON'
me2.pitch = 45
me2.velocity = 0


dt3 = midi.DeltaTime(mt)
dt3.time = 1024 * 2 * 2

me3 = midi.MidiEvent(mt)
me3.type = 'NOTE_ON'
me3.pitch = 45
me3.velocity = 94

dt4 = midi.DeltaTime(mt)
dt4.time = 1024 * 2 * 2 * 2 * 2

me4 = midi.MidiEvent(mt)
me4.type = 'NOTE_ON'
me4.pitch = 45
me4.velocity = 0



# n = midi.translate.midiEventsToNote([dt1, me1, dt2, me2])

m = note21.Note()

m2 = note21.Note()

midi.translate.midiEventsToNote([dt1, me1, dt2, me2], inputM21=m)

midi.translate.midiEventsToNote([dt3, me3, dt4, me4], inputM21=m2)

s1 = stream21.Stream()

s1.append(m)

s1.append(m2)

# s1.show()

# exit(0)

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

defaultTicksPerQuarter = 1024  # default

notes = []


def get_note(ref_note):
    return notes[ref_note]


ticks = []
events_midi = []

testing = pd.DataFrame(
    dict(
        index=list(range(100)),
        count=[0 for i in range(100)]
    )
)

# acc_ticks = 0

tick_last = 0

# acc_test = 0

duration_last = 0

for part in stream:
    for note in part.notes:
        if note.volume.velocity == 0:
            print('stop here')


counter = 0

tick_starts = []

# TODO: make hash table to count exactly which ticks are being counted twice

sum_ticks = 0

stream_recovered = stream21.Stream()

mt = midi.MidiTrack(1)

for part in stream:
    duration_entire_ticks = midi.translate.durationToMidi(part.duration)

    keys = [i for i in range(duration_entire_ticks)]

    counter_dict = {key: 0 for key in keys}

    for note in part.notes:
        m = note21.Note()

        # m2 = note.Note()

        dt1 = midi.DeltaTime(mt)

        ticks_offset = int(round(note.offset * defaultTicksPerQuarter))

        if ticks_offset < 0:
            debug = 1

        # dt1.time = ticks_offset  # midi.translate.noteToMidiEvents(note)[0].time
        dt1.time = midi.translate.noteToMidiEvents(note)[0].time

        me1 = midi.MidiEvent(mt)
        me1.type = 'NOTE_ON'
        me1.pitch = midi.translate.noteToMidiEvents(note)[1].pitch
        me1.velocity = midi.translate.noteToMidiEvents(note)[1].velocity

        dt2 = midi.DeltaTime(mt)
        dt2.time = midi.translate.noteToMidiEvents(note)[2].time

        me2 = midi.MidiEvent(mt)
        me2.type = 'NOTE_ON'
        me2.pitch = midi.translate.noteToMidiEvents(note)[3].pitch
        me2.velocity = midi.translate.noteToMidiEvents(note)[3].pitch

        midi.translate.midiEventsToNote([dt1, me1, dt2, me2], inputM21=m)

        # midi.translate.midiEventsToNote([dt3, me3, dt4, me4], inputM21=m2)

        # s1 = stream.Stream()

        stream_recovered.append(m)

        thing = midi.translate.noteToMidiEvents(note)[0]
        tick_starts.append(note.midiTickStart)

        # if note.duration > 0 and
        notes.append(note)
        # bug in music21 - no object _quarterLengthNeedsUpdating
        offset_ticks = int(round(note.offset * defaultTicksPerQuarter))
        # offset_ticks = note.midiTickStart
        duration_ticks = midi.translate.durationToMidi(note.duration)

        sum_ticks += duration_ticks

        for tick_empty in range(offset_ticks - tick_last):
            counter += 1
            counter_dict[tick_empty] = counter_dict[tick_empty] + 1
            ticks.append(tick_last + tick_empty)
            events_midi.append(None)

        computed_offset = counter

        # diffs.append(np.abs(computed_offset - offset_ticks))

        # assert that computed_offset == offset_ticks

        # end_last_note = tick_last + duration_last

        # acc_test = offset_ticks - end_last_note

        ref_note = len(notes) - 1
        # acc_ticks += duration_ticks
        for tick in range(duration_ticks):
            counter += 1
            counter_dict[tick] = counter_dict[tick] + 1
            ticks.append(offset_ticks + tick)
            events_midi.append(ref_note)

        tick_last = offset_ticks + duration_ticks

            # ticks[duration_offset + tick] = ref_note
        # print(note)


stream.show('midi')
# stream_recovered.show('midi')

# fp = stream_recovered.write('midi', fp='/Users/elliottevers/Downloads/stream_recovered.mid')

# add ticks for previous note based on offset

# len(ticks) == duration_entire_ticks

exit(0)



# stream.show()


# NOT ACCOUNTING FOR NON_LEGATO PLAYING

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


# TODO: convert notes to midi events

# check - delta time current + duration last = offset current

# TODO: write midi file using dataframe of ticks and events

# create track

# add event to track


mf = midi.translate.streamToMidiFile(stream)

print(len(mf.tracks[0].events))

# stream.plot('histogram', 'duration')