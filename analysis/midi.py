from music21 import analysis, stream


def key_center_windowed_complete(
    part,
    window_size_measures
):

    analyzer = analysis.discrete.BellmanBudge()

    wa = analysis.windowed.WindowedAnalysis(part, analyzer)

    solutions, color = wa.analyze(
        window_size_measures,
        'overlap'
    )

    return solutions
