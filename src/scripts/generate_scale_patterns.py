import sys
sys.path.insert(0, '/Users/elliottevers/Documents/git-repos.nosync/tk_music_py/src')

from music21 import scale as sc, pitch


flatten = lambda l: [item for sublist in l for item in sublist]


def in_thirds(scale_midi):
    return flatten([[p_midi, scale_midi[i + 2]] for i, p_midi in enumerate(scale_midi) if i < len(scale_midi) - 2])


def in_fifths(scale_midi):
    return flatten([[p_midi, scale_midi[i + 3]] for i, p_midi in enumerate(scale_midi) if i < len(scale_midi) - 3])


def main():
    edgeList = ['P5'] * 6 + ['d6'] + ['P5'] * 5
    net5ths = sc.intervalNetwork.IntervalNetwork()
    net5ths.fillBiDirectedEdges(edgeList)
    scales_over_fiths = [sc.MajorScale(p) for p in net5ths.realizePitch(pitch.Pitch('C1'))]

    print('in seconds')
    for scale in [s.getPitches('g2', 'f5', direction='ascending') for s in scales_over_fiths]:
        print([p.midi for p in scale])

    print('in thirds')
    for scale in [s.getPitches('g2', 'f5', direction='ascending') for s in scales_over_fiths]:
        print(in_thirds([p.midi for p in scale]))

    print('in fourths')
    for scale in [s.getPitches('g2', 'f5', direction='ascending') for s in scales_over_fiths]:
        print(in_fifths([p.midi for p in scale]))

if __name__ == '__main__':
    main()
