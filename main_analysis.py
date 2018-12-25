import filter.midi as filter
import convert.midi as midi_convert
import filter.series as series_filter
import mido
import pandas as pd
import itertools
import sys
import music21
from music21 import converter, graph, analysis
from mido import MetaMessage

from subprocess import call as call_shell

import seaborn as sns

import matplotlib.pyplot as plt

from subprocess import call as call_shell

filename_in = '/Users/elliottevers/Downloads/ella_dream_chords.mid'

filename_out = '/Users/elliottevers/Downloads/ella_dream_chords_doubled.mid'

stream = converter.parse(filename_in)

# filename_input = '/Users/elliottevers/Downloads/ella_dream_vocals_2.mid'

# filename_out = '/Users/elliottevers/Downloads/main.mid'

# bounds_graph_percentage = [0, 1]

# size_window = 4000

TRACK_CHORDS = 1

TRACK_BASS = 2

bpm_file = 75

file = mido.MidiFile(filename_in)

ppq = file.ticks_per_beat

track_chords = file.tracks[TRACK_CHORDS]

track_doubled = mido.MidiTrack()

track_doubled.append(
    MetaMessage(
        'time_signature',
        time=0
    )
)

track_doubled.append(
    MetaMessage(
        'set_tempo',
        tempo=mido.bpm2tempo(bpm_file),
        time=0
    )
)

for msg in track_chords:
    track_doubled.append(msg)

for msg in track_chords:
    if not msg.is_meta:
        track_doubled.append(msg)

file_out = mido.MidiFile(ticks_per_beat=ppq)

file_out.tracks.append(track_doubled)

file_out.save(filename_out)

call_shell(['open', '-a', '/Applications/MidiYodi 2018.1.app/', filename_out])

exit(0)

df = midi_convert.mid_to_series(
    file.tracks[2]
)

df_padded = df.append(df, ignore_index=True).append(df, ignore_index=True).append(df, ignore_index=True)

track = midi_convert.series_to_mid(
    df_padded,
    90
)

file_out = mido.MidiFile()

file_out.tracks.append(track)

file_out.save(filename_out)

call_shell(['open', '-a', '/Applications/MidiYodi 2018.1.app/', filename_out])

# call_shell(['open', '-a', '/Applications/MidiYodi 2018.1.app/', filename_in])

exit(0)

# p = graph.plot.WindowedKey(stream.parts[0])
#
# p.processorClass = analysis.discrete.BellmanBudge

# p.doneAction = 'show'

# p.run()

# solutions = p.processor.solutionsFound

# testing = 1

analyzer = analysis.discrete.BellmanBudge()

wa = analysis.windowed.WindowedAnalysis(stream.parts[0], analyzer)

# create pandas series, turn into midi using convert

# specifications

# parameters - choose quarter length

# at that granularity, create track of of key center sequence

# solutions, colors, meta = wa.process(
#     minWindow=2,
#     maxWindow=2,
#     windowStepSize=64,
#     windowType='adjacentAverage',
#     includeTotalWindow=False
# )

# 64 seems to work well
solutions, color = wa.analyze(
    64,
    'overlap'
)

testing = 1
