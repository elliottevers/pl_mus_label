import pandas as pd
from typing import List, Dict, Any, Optional, Tuple
import music21


def melody_to_df(data_melody, index_type='s'):
    list_melody = data_melody[1]

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

    df_segments = pd.DataFrame(
        data={
            'segment': [
                segment['label']
                for segment
                in segments
            ]
        },
        index=[
            segment['timestamp'] for segment in segments
        ]
    )

    df_segments.index.name = index_type

    return df_segments


def extract_tempomap(data_tempo):
    return data_tempo[1]


def extract_beatmap(data_beats):
    return [beat['timestamp'] for beat in data_beats]
