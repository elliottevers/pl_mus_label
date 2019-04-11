import music21
from postprocess import music_xml as postp_mxl
import itertools
import numpy as np
import pandas as pd
from typing import List
from music import segment
from utils import utils


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

    measures_window_size = 2

    analyzer = music21.analysis.discrete.BellmanBudge()

    wa = music21.analysis.windowed.WindowedAnalysis(score, analyzer)

    solutions, color = wa.analyze(
        measures_window_size,
        'overlap'
    )

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

    solutions_beats = _assign_key_centers(solutions, measures_window_size)

    solutions_measures = utils.grouper(4, solutions_beats)

    solutions_measures_21 = []

    for solution_measure in solutions_measures:

        measure = music21.stream.Measure()

        for i_solution, name_solution in enumerate(list(solution_measure)):
            note_beat = music21.note.Note(
                pitch=music21.pitch.Pitch(
                    name=name_solution,
                    octave=4
                )
            )
            note_beat.duration = music21.duration.Duration(
                quarterLength=1
            )
            measure.insert(i_solution, note_beat)

        solutions_measures_21.append(measure)

    for measure in solutions_measures_21:
        part_key_centers.append(measure)

    return part_key_centers


def _assign_key_centers(solutions, measures_window_size) -> List:
    beats = []

    num_measures = (len(solutions) + measures_window_size - 1) / 4

    num_beats = num_measures * 4

    for i_beat in range(0, int(num_beats)):
        beats.append([])

    for i_solution, solution in enumerate(solutions):
        for i_measure in range(0, measures_window_size):
            beats[i_solution + i_measure].append(solution.pitch.name)

    for i_beat in range(0, int(num_beats)):
        beats[i_beat] = utils.most_common(beats[i_beat])

    return beats


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



