from madmom.audio.chroma import DeepChromaProcessor
from madmom.features.chords import DeepChromaChordRecognitionProcessor

dcp = DeepChromaProcessor()

decode = DeepChromaChordRecognitionProcessor()

# chroma = dcp('/Users/elliottevers/Downloads/Miley_Cyrus_-_Malibu_Official_Video-8j9zMok6two.wav')

chroma = dcp('/Users/elliottevers/Downloads/Ella_Fitzgerald_-_All_The_Things_You_Are_with_lyrics-OPapxr8GvGA.wav')

stuff = decode(chroma)

test = 1

# import vamp
# import librosa
# data, rate = librosa.load("ccr.wav")
# chords = vamp.collect(data, rate, 'nnls-chroma:chordino')
#
# test = 1