import vamp
import librosa
from mido import MidiFile, MidiTrack, Message, MetaMessage
from typing import List, Dict, Any, Optional, Tuple
import music21
import numpy as np

data, rate = librosa.load("/Users/elliottevers/Documents/git-repos.nosync/audio/tswift.wav")

# TODO: melody extraction
melody = vamp.collect(data, rate, "mtg-melodia:melodia")

type(melody['vector'][1])

testing = 1

# TODO: segments - quantize to nearest two bar multiple
# import vamp
# import librosa
# segments = vamp.collect(data, rate, 'qm-vamp-plugins:qm-segmenter')

# test = 1

# TODO: chords
# ms_to_label_chord: List[Dict[float, Any]] = vamp.collect(data, rate, 'nnls-chroma:chordino')['list']

# ms_to_label_chord: List[Dict[float, Any]] = vamp.collect(data, rate, 'nnls-chroma:chordino')['list']

# testing = 1

# TODO: rolling tempo estimate

# tempo: List[Dict[float, Any]] = vamp.collect(data, rate, 'vamp-aubio:aubiotempo', 'tempo')['vector'][1]
# bpm = np.median(tempo)  # smoothing
# testing = 1

# TODO: measures

# beats: List[Dict[float, Any]] = vamp.collect(data, rate, 'qm-vamp-plugins:qm-barbeattracker')['list']
#
# testing = 1

# TODO: music21 chord parsing

# chord = music21.harmony.ChordSymbol(ms_to_label_chord[1]['label'].replace('b', '-'))
# chord.pitches  # ...

# for ms timeseries, treat bar estimates as framework to quantize segments and chords to
# TODO: symbolic segmentation - music21.search.segment.indexScoreParts?
testing = 1
