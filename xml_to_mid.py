from music21 import converter, midi

s = converter.parse('body_and_soul.mxl')

m = midi.translate.streamToMidiFile(s)

fp = m.write('midi', fp='body_and_soul.mid')

# s.show('midi')

# sm = midi.realtime.StreamPlayer(s)
#
# sm.play()

test = 1

