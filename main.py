import filter.midi as filter
import convert.midi as midi
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

df, boundaries = midi.mid_to_series(
    file.tracks[0]
)

# import seaborn as sns
#
# import matplotlib.pyplot as plt
#
# sns.relplot(kind="line", data=df[1:500_000])
#
# plt.show()
#
# exit(0)

output_mid = mido.MidiFile()

output_track = midi.series_to_mid(
    df,
    90
)

output_mid.tracks.append(output_track)

file.save('/Users/elliottevers/Downloads/main.mid')
