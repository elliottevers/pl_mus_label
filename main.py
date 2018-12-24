import filter.midi as filter
import convert.midi as midi_convert
import filter.series as series_filter
import mido
import pandas as pd
import itertools
import sys

from subprocess import call as call_shell

filename_input = '/Users/elliottevers/Downloads/ella_dream_vocals_2.mid'

####

file = mido.MidiFile(ticks_per_beat=2)


track1 = mido.MidiTrack()

file.tracks.append(track1)

track1.append(
    mido.MetaMessage(
        'set_tempo',
        tempo=500000*2*2
    )
)


track2 = mido.MidiTrack()

file.tracks.append(track2)

track2.append(
    mido.MetaMessage(
        'set_tempo',
        tempo=500000*2*2
    )
)


track3 = mido.MidiTrack()

file.tracks.append(track3)

track3.append(
    mido.MetaMessage(
        'set_tempo',
        tempo=500000*2*2
    )
)


track4 = mido.MidiTrack()

file.tracks.append(track4)

track4.append(
    mido.MetaMessage(
        'set_tempo',
        tempo=500000*2*2
    )
)

track1.append(
    mido.Message(
        'note_on',
        note=60,
        velocity=90,
        time=0
    )
)

track1.append(
    mido.Message(
        'note_off',
        note=60,
        velocity=0,
        time=1
    )
)

track1.append(
    mido.Message(
        'note_on',
        note=67,
        velocity=90,
        time=1
    )
)

track1.append(
    mido.Message(
        'note_off',
        note=67,
        velocity=0,
        time=1
    )
)


track2.append(
    mido.Message(
        'note_on',
        note=60,
        velocity=90,
        time=0
    )
)

track2.append(
    mido.Message(
        'note_off',
        note=60,
        velocity=0,
        time=1
    )
)

track2.append(
    mido.Message(
        'note_on',
        note=67,
        velocity=90,
        time=0
    )
)

track2.append(
    mido.Message(
        'note_off',
        note=67,
        velocity=0,
        time=2
    )
)

track3.append(
    mido.Message(
        'note_on',
        note=60,
        velocity=90,
        time=0
    )
)

track3.append(
    mido.Message(
        'note_on',
        note=67,
        velocity=90,
        time=1
    )
)

track3.append(
    mido.Message(
        'note_off',
        note=60,
        velocity=0,
        time=1
    )
)

track3.append(
    mido.Message(
        'note_off',
        note=67,
        velocity=0,
        time=1
    )
)

track4.append(
    mido.Message(
        'note_on',
        note=60,
        velocity=90,
        time=0
    )
)

track4.append(
    mido.Message(
        'note_on',
        note=67,
        velocity=90,
        time=1
    )
)

track4.append(
    mido.Message(
        'note_off',
        note=67,
        velocity=0,
        time=1
    )
)

track4.append(
    mido.Message(
        'note_off',
        note=60,
        velocity=0,
        time=1
    )
)

filename_out = '/Users/elliottevers/Downloads/simulated_data.mid'

file.save(filename_out)

call_shell(["open", "-a", "/Applications/MidiYodi 2018.1.app/", filename_out])

exit(0)
####

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
