import music21
from typing import List
from utils import utils
from postprocess import music_xml as postp_mxl


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


def get_segments(
    part: music21.stream.Part,
) -> music21.stream.Part:

    segments, measure_lists = music21.search.segment.translateMonophonicPartToSegments(
        part.makeMeasures()
        # TODO: add this back in
        # postp_mxl.extract_part(
        #     score,
        #     'melody'
        # )
    )

    part = music21.stream.Part()

    part.id = 'segment'

    for list_measure in measure_lists:

        note_segment = music21.note.Note()

        if list_measure[1] - list_measure[0] == 0:
            continue

        note_segment.duration = music21.duration.Duration(
            (list_measure[1] - list_measure[0]) * 4
        )

        notes_already_in_segment = part.getElementsByOffset(
            offsetStart=list_measure[0]*4,
            offsetEnd=list_measure[1]*4,
            includeEndBoundary=False,
            mustBeginInSpan=False,
            includeElementsThatEndAtStart=False
        )

        pitches_in_segment = [note.pitch.midi for note in notes_already_in_segment]

        note_segment.pitch = music21.pitch.Pitch(
            max(pitches_in_segment) + 12 if 60 in pitches_in_segment else 60

        )

        part.insert(list_measure[0] * 4, note_segment)

    return part
