import pandas as pd
import numpy as np
from typing import Dict, Any, List
import music21


# def beatmap_to_ts(beatmap: List[float]):
def beatmap_to_ts(beatmap):
    return dict(
        zip(
            beatmap.tolist(),
            [music21.note.Note('C') for _ in range(len(beatmap.tolist()))]
        )
    )


def monophony_to_df(data_monophonic, name_part, index_type='s'):
    list_monophony = data_monophonic[1]

    if not isinstance(data_monophonic[0], float):
        sample_rate = data_monophonic[0].to_float()
    else:
        sample_rate = data_monophonic[0]

    df_mid = pd.DataFrame(
        data={name_part: list_monophony},
        index=[i_sample * sample_rate for i_sample, sample in enumerate(list_monophony)]
    )

    df_mid.index.name = index_type

    return df_mid


def melody_to_df(data_melody, index_type='s'):
    list_melody = data_melody[1]

    if not isinstance(data_melody[0], float):
        sample_rate = data_melody[0].to_float()
    else:
        sample_rate = data_melody[0]

    df_melody_hz = pd.DataFrame(
        data={'melody': list_melody},
        index=[i_sample * sample_rate for i_sample, sample in enumerate(list_melody)]
    )

    df_melody_hz.index.name = index_type

    return df_melody_hz


def chords_to_df(chords: Dict[Any, music21.chord.Chord], index_type='s'):
    df_chords = pd.DataFrame(
        data={'chord': list(chords.values())}, index=list(chords.keys())
    )

    df_chords.index.name = index_type

    return df_chords


def segments_to_df(data_segments, index_type='s'):

    segments = [
        {
            'timestamp': segment['timestamp'],
            'duration': segment['duration'],
            'label': segment['label']
        }
        for segment
        in data_segments
    ]

    data = [
        segment['label']
        for segment
        in segments
    ]

    index = [
        segment['timestamp'].to_float() for segment in segments
    ]

    df_segments = pd.DataFrame(
        data={
            'segment': data
        },
        index=index
    )

    df_segments.index.name = index_type

    return df_segments


def ts_beatmap_to_df(beatmap: Dict[Any, music21.note.Note], index_type='s'):
    df_beatmap = pd.DataFrame(
        data={'beatmap': list(beatmap.values())}, index=list(beatmap.keys())
    )

    df_beatmap.index.name = index_type

    return df_beatmap


def extract_tempomap(data_tempo):
    return data_tempo[1]


def to_tempo(data_tempo):
    return np.median(
        [
            float(string_nonempty)
            for string_nonempty
            in [el['label'].replace(' bpm', '') for el in data_tempo['list']]
            if string_nonempty
        ]
    )


def extract_beatmap(data_beats):
    return [
        beat['timestamp'] for beat in data_beats['list']
    ]
