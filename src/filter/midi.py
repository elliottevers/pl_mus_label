import mido
from mido import Message, MetaMessage, MidiTrack
import pandas as pd
import itertools


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


# TODO: let's implement so kind of filtering based on quantization

def smooth_chords(df: pd.DataFrame, cadence_beats=4) -> pd.DataFrame:
    chords_smoothed = []

    # NB: we assume here that the first level of index is "beat"
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


def smooth_bass(df: pd.DataFrame, cadence_beats=1) -> pd.DataFrame:
    bass_smoothed = []

    for index, row in df.itertuples(index=True, name='bass'):
        if index[0] % 4 == 1:
            bass_smoothed.append(df.loc[(index[0] + 1, slice(None)), 'bass'].values[0])
        elif index[0] % 4 == 0:
            bass_smoothed.append(df.loc[(index[0] - 1, slice(None)), 'bass'].values[0])
        else:
            bass_smoothed.append(df.loc[(index[0], slice(None)), 'bass'].values[0])

    df_smoothed = df
    df_smoothed['bass'] = bass_smoothed
    return df_smoothed


def smooth_segment(df: pd.DataFrame, cadence_beats=16) -> pd.DataFrame:
    segment_smoothed = []

    for index, row in df.itertuples(index=True, name='segment'):
        if index[0] % 4 == 1:
            segment_smoothed.append(df.loc[(index[0] + 1, slice(None)), 'segment'].values[0])
        elif index[0] % 4 == 0:
            segment_smoothed.append(df.loc[(index[0] - 1, slice(None)), 'segment'].values[0])
        else:
            segment_smoothed.append(df.loc[(index[0], slice(None)), 'segment'].values[0])

    df_smoothed = df
    df_smoothed['segment'] = segment_smoothed
    return df_smoothed

