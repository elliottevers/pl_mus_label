import vamp
import librosa
data, rate = librosa.load("ccr.wav")
segments = vamp.collect(data, rate, 'qm-vamp-plugins:qm-segmenter')

test = 1