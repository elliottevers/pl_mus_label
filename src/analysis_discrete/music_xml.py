import music21
from postprocess import music_xml as postp_mxl
import itertools
import numpy as np
import pandas as pd
from typing import List
from music import segment


# def key_center_windowed_complete(
#     part,
#     measures_window_size
# ):
#
#     analyzer = music21.analysis.discrete.BellmanBudge()
#
#     wa = music21.analysis.windowed.WindowedAnalysis(part, analyzer)
#
#     solutions, color = wa.analyze(
#         measures_window_size,
#         'overlap'
#     )
#
#     return solutions


def get_key_center_estimates(
    score: music21.stream.Score,
    measures_window_size: int = 64
) -> music21.stream.Part:

    analyzer = music21.analysis.discrete.BellmanBudge()

    wa = music21.analysis.windowed.WindowedAnalysis(score, analyzer)

    solutions, color = wa.analyze(
        measures_window_size,
        'overlap'
    )

    num_measures = (len(solutions) + measures_window_size - 1) / 2

    part_key_centers = music21.stream.Part()

    solutions = [
        music21.note.Note(
            music21.pitch.Pitch(
                midi=tuple_pitch[0].midi
            )
        )
        for tuple_pitch
        in solutions
    ]

    for i_measure in range(1, int(num_measures)):
        part_key_centers.append(solutions[i_measure])

    return part_key_centers


def _get_notes_segments(segments, measure_lists):
    measure_number_last = measure_lists[-1][1]

    measures: List[List[int]] = []

    note_mapper = segment.SegmentNoteMapper()

    for index_measure in range(1, measure_number_last + 1):
        segments_overlapping = segment.SegmentNoteMapper.get_segments_overlapping(index_measure, measure_lists, segments)
        note_mapper.add(segments_overlapping)
        pitches = note_mapper.get_current_pitches()
        measures.append(pitches)

    return measures


def _measures_to_score(measures: List[List[music21.note.Note]], name_part) -> music21.stream.Score:

    part = music21.stream.Part()

    part.id = name_part

    for notes in measures:

        measure_21 = music21.stream.Measure()

        if len(notes) > 1:
            note = music21.chord.Chord(notes=notes)
        elif len(notes) == 1:
            note = notes[0]
        else:
            note = music21.note.Rest()

        note.duration = music21.duration.Duration(4.0)
        measure_21.append(note)
        part.append(measure_21)

    score = music21.stream.Score()

    score.insert(0, part)

    return score


def get_segments(
    score: music21.stream.Score,
    name_part
) -> music21.stream.Score:

    segments, measure_lists = music21.search.segment.translateMonophonicPartToSegments(
        score.parts[0]
    )

    return _measures_to_score([
            [music21.note.Note(pitch=music21.pitch.Pitch(midi=pitch)) for pitch in measure]
            for measure
            in _get_notes_segments(segments, measure_lists)
        ],
        name_part=name_part
    )



