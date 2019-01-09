import filter.midi as filter
import convert.midi as midi_convert
import filter.series as series_filter, filter.midi as midi_filter, analysis.midi as midi_analysis
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

# filename_in = '/Users/elliottevers/Downloads/ella_dream_chords.mid'

# filename_out = '/Users/elliottevers/Downloads/ella_dream_chords_doubled.mid'

filename_in = '/Users/elliottevers/Downloads/Chordify_It-Wasn-t-God-Who-Made-Honky-Tonk-Angels-Kitty-Wells_Quantized_at_136_BPM.mid'

filename_out = '/Users/elliottevers/Downloads/kitty_honky_chords_doubled.mid'

# stream = converter.parse(filename_in)

# filename_input = '/Users/elliottevers/Downloads/ella_dream_vocals_2.mid'

# filename_out = '/Users/elliottevers/Downloads/main.mid'

# bounds_graph_percentage = [0, 1]

# size_window = 4000

TRACK_CHORDS = 1  # 1

TRACK_BASS = 2  # 2

bpm_file = 136  # 75

file = mido.MidiFile(filename_in)

ppq = file.ticks_per_beat

track_chords = file.tracks[TRACK_CHORDS]

track_doubled = midi_filter.pad(
    track_chords,
    bpm_file,
    2
)

file_out = mido.MidiFile(ticks_per_beat=ppq)

file_out.tracks.append(track_doubled)

file_out.save(filename_out)

call_shell(['open', '-a', '/Applications/MidiYodi 2018.1.app/', filename_out])

exit(0)

filename_in = '/Users/elliottevers/Downloads/ella_dream_chords_doubled.mid'

stream = converter.parse(filename_in)

# solutions = midi_analysis.key_center_windowed_complete(
#     part=stream,
#     window_size_measures=64,
#     melody=True
# )

# analyzer = analysis.discrete.BellmanBudge()
#
# wa = analysis.windowed.WindowedAnalysis(stream.parts[0], analyzer)
#
# solutions, color = wa.analyze(
#     64,
#     'overlap'
# )

# (len(solutions) + 64 - 1)/2

num_measures = 230

notes = []

# for i_measure in range(1, num_measures):
#     notes.append(solutions[i_measure][0].midi)

solutions = [60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 60, 60, 60, 60, 60, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 65, 65, 70, 70, 70, 70, 70, 70, 70, 70, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60]

# generate midi track of tones

# figure out how many ticks to make each note - ppq of track to "overdub"

# listen to track together for validation

file_overdubbed = mido.MidiFile(ticks_per_beat=ppq)

track_main = track_chords

track_overdub = mido.MidiTrack()

track_overdub.append(
    MetaMessage(
        'time_signature',
        time=0
    )
)

track_overdub.append(
    MetaMessage(
        'set_tempo',
        tempo=mido.bpm2tempo(bpm_file),
        time=0
    )
)

velocity = 90

for pitch_midi in solutions:
    track_overdub.append(
        mido.Message(
            'note_on',
            note=pitch_midi,
            velocity=velocity,
            time=0
        )
    )
    track_overdub.append(
        mido.Message(
            'note_off',
            note=pitch_midi,
            velocity=0,
            time=ppq
        )
    )

file_overdubbed.tracks.append(track_main)

file_overdubbed.tracks.append(track_overdub)

filename_out = '/Users/elliottevers/Downloads/ella_dream_chords_and_key_centers.mid'

file_overdubbed.save(filename_out)

call_shell(['open', '-a', '/Applications/MidiYodi 2018.1.app/', filename_out])

# print(notes)

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
