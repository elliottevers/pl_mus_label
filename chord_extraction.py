from madmom.audio.chroma import DeepChromaProcessor
from madmom.features.chords import DeepChromaChordRecognitionProcessor

dcp = DeepChromaProcessor()

decode = DeepChromaChordRecognitionProcessor()

chroma = dcp('ccr.wav')

stuff = decode(chroma)

# test = 1