from music21 import midi, converter, environment, tempo, note
from music21 import note as note21, stream as stream21, analysis, graph
from mido import MidiFile
import mido
import pandas as pd

import os

import numpy as np
import pandas as pd
import matplotlib
import sys

filename_input = '/Users/elliottevers/Downloads/output_midi_to_ticks_timeseries.mid'

# mf = midi.MidiFile()
#
# mf.open(str(filename_input))
# mf.read()
# mf.close()
#
# s = midi.translate.midiFileToStream(mf)

note.Note

d = duration.Duration()

midi.translate.midiToDuration(duration_ticks)

stream = converter.parse(filename_input)

stream.show('midi')