from music21 import *



stream = stream.Stream()

duration1 = duration.Duration(1)

duration2 = duration.Duration(1)

note1 = note.Note(
    'A'
)

# note1.offset = 1

note2 = note.Note(
    'B'
)

note3 = note.Note(
    'C'
)

# note2.offset = 3

# stream.append(note1)

# stream.append(note2)

stream.insert(0, note1)

stream.insert(2, note2)

stream.insert(4, note3)

stream.makeRests(fillGaps=True, inPlace=False, hideRests=True)

stream.show()


