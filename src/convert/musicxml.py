import pandas as pd
import music21
from typing import List, Dict, Any, Optional, Tuple
from music import note as lib_note, song, chord as lib_chord


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
    beat_last = max(df_grans.index.get_level_values(column_index))

    parts = []

    for name_part, position in partmap.items():
        part = music21.stream.Part()
        part.id = name_part
        parts.append(part)

    part = parts[0]

    measure = music21.stream.Measure()

    # TODO: HAVE to make more efficient
    for i, note in df_grans.itertuples(index=True, name=True):
        beat = i[0]
        s = i[1]

        if beat == int(beat):
            part.append(measure)
            measure = music21.stream.Measure()

        if note is None:
            note = music21.note.Rest()
        else:
            note = music21.note.Note(pitch=note.pitch)

        note.duration = music21.duration.Duration(1/48)
        measure.append(
            note
        )

    score = music21.stream.Score()

    score.insert(0, part)

    return score

