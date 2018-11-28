# from madmom.audio.chroma import DeepChromaProcessor
# from madmom.features.chords import DeepChromaChordRecognitionProcessor
#
# dcp = DeepChromaProcessor()
#
# decode = DeepChromaChordRecognitionProcessor()
#
# chroma = dcp('ccr.wav')
#
# stuff = decode(chroma)
#
# # test = 1

import vamp
import librosa
data, rate = librosa.load("ccr.wav")
chords = vamp.collect(data, rate, 'nnls-chroma:chordino')

test = 1