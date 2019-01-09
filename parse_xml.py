from music21 import *
path_file = '/Users/elliottevers/Desktop/pg_music_export_2.XML'
b = converter.parse(path_file)
partStream = b.parts.stream()

# get parts 1 and 2, flatten into single part, conduct harmonic analysis
# stream.mergeElements(
part_bass = partStream[0]
# b.show()
testing = 1

# TODO: what if we

