import pandas as pd
import music21
from typing import List, Dict, Any, Optional, Tuple
from music import note as lib_note, song, chord as lib_chord
import numpy as np


def df_beats_to_score(df: pd.DataFrame, column_index='beat', partmap={'chord': 0}) -> music21.stream.Score:

    beat_last = max(df.index.get_level_values(column_index))

    parts = []

    for name_part, position in partmap.items():
        part = music21.stream.Part()
        part.id = name_part
        parts.append(part)

    part = parts[0]

    measure = music21.stream.Measure()

    for beat in range(1, beat_last):
        if beat % 4 == 1:
            part.append(measure)
            measure = music21.stream.Measure()
        chord: lib_chord.ChordMidi = df.loc[(beat, slice(None)), 'chord'].values[0]
        measure.append(
            music21.chord.Chord(
                [music21.pitch.Pitch(midi=chord_midi.pitch).name for chord_midi in chord.notes],
                duration=music21.duration.Duration(1.0)
            )
        )

    score = music21.stream.Score()

    score.insert(0, part)

    return score


def df_grans_to_score(df_grans: pd.DataFrame, column_index='beat', partmap={'melody': 0}) -> music21.stream.Score:
    parts = []

    for name_part, position in partmap.items():
        part = music21.stream.Part()
        part.id = name_part
        parts.append(part)

    part = parts[0]

    df_grans['event'] = (df_grans['melody'].shift(1) != df_grans['melody']).astype(int).cumsum()

    df_events = df_grans.reset_index().groupby(['melody','event'])[column_index].apply(np.array)

    beat_to_note = dict()

    for i, span in df_events.iteritems():
        pitch_midi = i[0]
        beat_start = span[0]
        beat_end = span[-1]
        duration = beat_end - beat_start + 1/48

        duration = music21.duration.Duration(duration)

        if not pitch_midi > 0:
            note = music21.note.Rest(duration=duration)
        else:
            note = music21.note.Note(pitch=music21.pitch.Pitch(midi=int(pitch_midi)), duration=duration)

        beat_to_note[beat_start] = note

    measure = music21.stream.Measure()

    for beat in df_grans.index.get_level_values(0).tolist():
        if int(beat) == beat and int(beat) % 4 == 0:
            part.append(measure)
            measure = music21.stream.Measure()

        if beat in beat_to_note:
            note = beat_to_note[beat]
            measure.append(
                note
            )

    score = music21.stream.Score()

    score.insert(0, part)

    return score

