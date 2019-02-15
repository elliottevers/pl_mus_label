import mido
from mido import Message, MetaMessage, MidiTrack
import pandas as pd
import itertools


# def filter_length(
#         divisor_quarter_note,
#         track_to_filter,
#         ppq,
#         bpm
# ):

def pad(
    track,
    bpm,
    num_copies=2
):

    track_padded = mido.MidiTrack()

    track_padded.append(
        MetaMessage(
            'time_signature',
            time=0
        )
    )

    track_padded.append(
        MetaMessage(
            'set_tempo',
            tempo=mido.bpm2tempo(bpm),
            time=0
        )
    )

    for _ in itertools.repeat(None, num_copies):
        for msg in track:
            if not msg.is_meta:
                track_padded.append(msg)

    return track_padded



def smooth_chords(df: pd.DataFrame) -> pd.DataFrame:
    chords_smoothed = []
    for index, row in df.itertuples(index=True, name='chord'):
        if index[0] % 4 == 1:
            chords_smoothed.append(df.loc[(index[0] + 1, slice(None)), 'chord'].values[0])
        elif index[0] % 4 == 0:
            chords_smoothed.append(df.loc[(index[0] - 1, slice(None)), 'chord'].values[0])
        else:
            chords_smoothed.append(df.loc[(index[0], slice(None)), 'chord'].values[0])

    df_smoothed = df
    df_smoothed['chord'] = chords_smoothed
    return df_smoothed
