import filter.midi as filter
import convert.midi as midi_convert
import filter.series as series_filter
import mido
import pandas as pd

filename_input = '/Users/elliottevers/Downloads/ella_dream_vocals_2.mid'

bpm_file = 75

file = mido.MidiFile(filename_input)

ppq = file.ticks_per_beat

# df = filter.filter_length(
#     4,
#     file.tracks[0],
#     ppq,
#     bpm_file
# )

df, boundaries = midi_convert.mid_to_series(
    file.tracks[0]
)

# def filter_note_length(
#         df,
#         divisor_quarter_note,
#         ppqd,
#         bpm
# ):
#     return True

# df = series_filter.filter_note_length(
#     df,
#     boundaries,
#     divisor_quarter_note=4,
#     ppq=ppq
# )

import seaborn as sns

import matplotlib.pyplot as plt

sns.relplot(kind="line", data=df.loc[407:419])

plt.show()

exit(0)

output_mid = mido.MidiFile(ticks_per_beat=file.ticks_per_beat)

output_track = midi_convert.series_to_mid(
    df,
    90
)

output_mid.tracks.append(output_track)

file.save('/Users/elliottevers/Downloads/main.mid')
