from music21 import midi, converter, environment, tempo
from music21 import note as note21, stream as stream21, analysis, graph
from mido import MidiFile
import mido
import pandas as pd

import numpy as np
import pandas as pd
import matplotlib
import sys

filename = '/Users/elliottevers/Downloads/kitty_honky_chords_doubled.mid'

stream = converter.parse(filename)

p = graph.plot.WindowedKey(stream.parts[0])

p.processorClass = analysis.discrete.BellmanBudge

# p.doneAction = 'show'
p.run()

# >>> p.processorClass = analysis.discrete.KrumhanslKessler
# >>> p.processorClass = analysis.discrete.AardenEssen
# >>> p.processorClass = analysis.discrete.SimpleWeights
# >>> p.processorClass = analysis.discrete.BellmanBudge
# >>> p.processorClass = analysis.discrete.TemperleyKostkaPayne

# bbAnalyzer = analysis.discrete.BellmanBudge()
#
# wa = analysis.windowed.WindowedAnalysis(stream.parts[0], bbAnalyzer)
#
#
# solutions, colors, meta = wa.process(
#     minWindow=4,
#     maxWindow=12,
#     windowStepSize=4,
#     windowType='overlap',
#     # windowType='adjacentAverage',
#     includeTotalWindow=False
# )
#
# print(p.processor.solutionsFound)


