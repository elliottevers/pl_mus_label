import vamp
import librosa
data, rate = librosa.load("ccr.wav")
keys = vamp.collect(data, rate, 'qm-vamp-plugins:qm-keydetector')

plugins = vamp.list_plugins()
test = 1
