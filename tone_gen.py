# import struct
# import numpy as np
# from scipy import signal as sg
#
# Fs = 44100                    ## Sampling Rate
# f = 440                       ## Frequency (in Hz)
# sample = 44100                ## Number of samples
# x = np.arange(sample)
#
# ####### sine wave ###########
# y = 100*np.sin(2 * np.pi * f * x / Fs)
#
# ####### square wave ##########
# # y = 100* sg.square(2 *np.pi * f *x / Fs )
#
# ####### square wave with Duty Cycle ##########
# # y = 100* sg.square(2 *np.pi * f *x / Fs , duty = 0.8)
#
# ####### Sawtooth wave ########
# # y = 100* sg.sawtooth(2 *np.pi * f *x / Fs )
#
#
# f = open('test.wav','wb')
# ## Open as Signed 8-bit on Audacity - Watch Video for instructions
#
# for i in y:
# 	print(i)
# 	f.write(struct.pack('b',i))
# f.close()

import collections
import wave, struct, math

ts_melody = '/Users/elliottevers/Downloads/lodi_melody_hz.txt'

ms_to_pitch = collections.OrderedDict()

in_ms = False

samples_per_second = 50.

step_size = 1 / samples_per_second

if in_ms:
    with open(ts_melody, 'r') as file_local:
        for line in file_local:
            value_hz = int(float(line.split()[1]))
            if value_hz > 0:
                ms_to_pitch[float(line.split()[0])] = int(float(line.split()[1]))
else:
    current_ms = 0
    with open(ts_melody, 'r') as file_local:
        for line in file_local:
            ms_to_pitch[float(current_ms)] = int(float(line.split()[1]))
            current_ms += step_size


sampleRate = 44100.0
duration = 1.0
frequency = 440.0

wavef = wave.open('/Users/elliottevers/Downloads/sound.wav','w')
wavef.setnchannels(1)
wavef.setsampwidth(2)
wavef.setframerate(sampleRate)

# ts_frequency = [440.0, 880.0]

gran_seconds = 1.0

span_time = 0.02

# for freq in ms_to_pitch:
for _, freq in ms_to_pitch.items()[1:10000]:
    for i in range(int(span_time * sampleRate)):
        value = int(32767.0*math.cos(freq*math.pi*float(i)/float(sampleRate)))
        data = struct.pack('<h', value)
        wavef.writeframesraw(data)

# for freq in ts_frequency:
#     for i in range(int(gran_seconds * sampleRate)):
#         value = int(32767.0*math.cos(freq*math.pi*float(i)/float(sampleRate)))
#         data = struct.pack('<h', value)
#         wavef.writeframesraw(data)

wavef.writeframes('')
wavef.close()
