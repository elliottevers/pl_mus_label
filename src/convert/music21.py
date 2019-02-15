import pandas as pd
import music21
from typing import List, Dict, Any, Optional, Tuple
from music import note as lib_note, song, chord as lib_chord


def df_to_score(df: pd.DataFrame, column_index='beat', partmap={'chord': 0}) -> music21.stream.Score:

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

    # part_chords = music21.stream.Part()
    #
    # part_bass = music21.stream.Part()
    #
    # measure1chords = music21.stream.Measure()
    #
    # measure2chords = music21.stream.Measure()
    #
    # measure1notes = music21.stream.Measure()
    #
    # measure2notes = music21.stream.Measure()
    #
    # measure1notes.append(
    #     music21.note.Note(
    #         pitch='C',
    #         duration=music21.duration.Duration(2.0)
    #     )
    # )
    #
    # measure1notes.append(
    #     music21.note.Note(
    #         pitch='D',
    #         duration=music21.duration.Duration(2.0)
    #     )
    # )
    #
    # measure2notes.append(
    #     music21.note.Note(
    #         pitch='C',
    #         duration=music21.duration.Duration(2.0)
    #     )
    # )
    #
    # measure2notes.append(
    #     music21.note.Note(
    #         pitch='D',
    #         duration=music21.duration.Duration(2.0)
    #     )
    # )
    #
    # measure1chords.append(
    #     music21.chord.Chord(
    #         ['E', 'G'],
    #         duration=music21.duration.Duration(2.0)
    #     )
    # )
    #
    # measure1chords.append(
    #     music21.chord.Chord(
    #         ['F', 'A'],
    #         duration=music21.duration.Duration(2.0)
    #     )
    # )
    #
    # measure2chords.append(
    #     music21.chord.Chord(
    #         ['E', 'G'],
    #         duration=music21.duration.Duration(2.0)
    #     )
    # )
    #
    # measure2chords.append(
    #     music21.chord.Chord(
    #         ['F', 'A'],
    #         duration=music21.duration.Duration(2.0)
    #     )
    # )
    #
    # part_chords.append(
    #     measure1chords
    # )
    #
    # part_chords.append(
    #     measure2chords
    # )
    #
    # part_bass.append(
    #     measure1notes
    # )
    #
    # part_bass.append(
    #     measure2notes
    # )
    #
    # score.parts.append(
    #     part_bass
    # )
    #
    # score.parts.append(
    #     part_chords
    # )
    #
    # score.insert(0, part_chords)
    # score.insert(0, part_bass)
    # raise 'not implemented'
