# plot the midi file

from music21 import midi, converter, environment

# us = environment.UserSettings()
# us.create()
#
# for key in sorted(us.keys()):
#     print(key)

# us = environment.UserSettings()
# print(us.getSettingsPath())

# environment.set('musescoreDirectPNGPath', '/Applications/MuseScore 2.app/Contents/MacOS/mscore')


# file_midi = midi.MidiFile()
#
# file_midi.open(
#     filename='/Users/elliottevers/Downloads/ella_dream_vocals.mid',
#     attrib='rb'
# )

# stream = midi.translate.midiFileToStream(
#     file_midi
# )

stream = converter.parse('/Users/elliottevers/Downloads/ella_dream_vocals.mid')

# stream.show('midi')

# stream.plot('histogram', 'pitch')

# stream.plot('histogram', 'duration')

# for note in stream:
#     for pitch in note.pitches:
#         print(pitch.midi)

# for note in stream.part.pitches:
#     print(note)

testing = 1

# stream.plot('pianoroll')


# TODO:
# plot parts of stream
# histogram to decide what value to initialize value of windowed average
# try starting with mean of entire score

# how to remove

notes_filtered = []

for part in stream:
    for note in part.notes:
        # stream.remove(note)
        notes_filtered.append(note)

stream.parts[0].remove(notes_filtered)

for part in stream:
    for note in part.notes:
        print(note)

stream.plot('histogram', 'duration')