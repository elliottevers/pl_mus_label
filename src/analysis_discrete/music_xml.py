import music21


def key_center_windowed_complete(
    part,
    measures_window_size
):

    analyzer = music21.analysis.discrete.BellmanBudge()

    wa = music21.analysis.windowed.WindowedAnalysis(part, analyzer)

    solutions, color = wa.analyze(
        measures_window_size,
        'overlap'
    )

    return solutions


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
