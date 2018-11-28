import vamp
import librosa
data, rate = librosa.load("ccr.wav")
tempo = vamp.collect(data, rate, 'vamp-example-plugins:fixedtempo')

plugins = vamp.list_plugins()
test = 1