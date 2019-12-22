import sys
sys.path.insert(0, '/Users/elliottevers/Documents/git-repos.nosync/tk_music_py/src')

from music21 import scale as sc, pitch


flatten = lambda l: [item for sublist in l for item in sublist]


def in_thirds_rise(scale_midi):
    return flatten([[p_midi, scale_midi[i + 2]] for i, p_midi in enumerate(scale_midi) if i < len(scale_midi) - 2])


def in_thirds_fall(scale_midi):
    return flatten([[scale_midi[i + 2], p_midi] for i, p_midi in enumerate(scale_midi) if i < len(scale_midi) - 2])


def in_fourths_rise(scale_midi):
    return flatten([[p_midi, scale_midi[i + 3]] for i, p_midi in enumerate(scale_midi) if i < len(scale_midi) - 3])


def in_fourths_fall(scale_midi):
    return flatten([[scale_midi[i + 3], p_midi] for i, p_midi in enumerate(scale_midi) if i < len(scale_midi) - 3])


def in_fifths_rise(scale_midi):
    return flatten([[p_midi, scale_midi[i + 4]] for i, p_midi in enumerate(scale_midi) if i < len(scale_midi) - 4])


def in_fifths_fall(scale_midi):
    return flatten([[scale_midi[i + 4], p_midi] for i, p_midi in enumerate(scale_midi) if i < len(scale_midi) - 4])


def in_triads_rise(scale_midi):
    return flatten([[p_midi, scale_midi[i + 2], scale_midi[i + 4]] for i, p_midi in enumerate(scale_midi) if i < len(scale_midi) - 4])


def in_triads_fall(scale_midi):
    return flatten([[scale_midi[i + 4], scale_midi[i + 2], p_midi] for i, p_midi in enumerate(scale_midi) if i < len(scale_midi) - 4])


def main():
    edgeList = ['P5'] * 6 + ['d6'] + ['P5'] * 5
    net5ths = sc.intervalNetwork.IntervalNetwork()
    net5ths.fillBiDirectedEdges(edgeList)
    scales_over_fiths = [sc.MajorScale(p) for p in net5ths.realizePitch(pitch.Pitch('C1'))]

    print('in seconds')
    for scale in [s.getPitches('g2', 'f5', direction='ascending') for s in scales_over_fiths]:
        print(str([p.midi for p in scale]) + ',')

    print('in thirds rising')
    for scale in [s.getPitches('g2', 'f5', direction='ascending') for s in scales_over_fiths]:
        print(str(in_thirds_rise([p.midi for p in scale])) + ',')

    print('in thirds falling')
    for scale in [s.getPitches('g2', 'f5', direction='ascending') for s in scales_over_fiths]:
        print(str(in_thirds_fall([p.midi for p in scale])) + ',')

    print('in fourths rising')
    for scale in [s.getPitches('g2', 'f5', direction='ascending') for s in scales_over_fiths]:
        print(str(in_fourths_rise([p.midi for p in scale])) + ',')

    print('in fourths falling')
    for scale in [s.getPitches('g2', 'f5', direction='ascending') for s in scales_over_fiths]:
        print(str(in_fourths_fall([p.midi for p in scale])) + ',')

    print('in fifths rising')
    for scale in [s.getPitches('g2', 'f5', direction='ascending') for s in scales_over_fiths]:
        print(str(in_fifths_rise([p.midi for p in scale])) + ',')

    print('in fifths falling')
    for scale in [s.getPitches('g2', 'f5', direction='ascending') for s in scales_over_fiths]:
        print(str(in_fifths_fall([p.midi for p in scale])) + ',')

    print('in triads rising')
    for scale in [s.getPitches('g2', 'f5', direction='ascending') for s in scales_over_fiths]:
        print(str(in_triads_rise([p.midi for p in scale])) + ',')

    print('in triads falling')
    for scale in [s.getPitches('g2', 'f5', direction='ascending') for s in scales_over_fiths]:
        print(str(in_triads_fall([p.midi for p in scale])) + ',')


if __name__ == '__main__':
    main()
