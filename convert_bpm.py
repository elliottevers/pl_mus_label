from mido import MidiFile
# read file's current bpm and resolution

# ticks_per_beat = 96
file_from = MidiFile('/Users/elliottevers/Documents/tracks/MelodyTracks/ella_dream_melody.mid')

# ticks_per_beat = 384
# tempo = 800_000
file_to = MidiFile('/Users/elliottevers/Documents/tracks/ChordTracks/ella_dream_chords.mid')

testing = 1

filename_out = '/Users/elliottevers/Documents/conversion_out.mid'

file_out = MidiFile()

#
# filename_overlay = 'lodi_master_raw_overlay.mid'
#
# midi_file_vocals = MidiFile('lodi_vocals.mid')
#
# track_vocals = midi_file_vocals.tracks[0]
#
# file_midi_master_raw.tracks.append(track_vocals)
#
# file_midi_master_raw.save(filename_overlay)
#
# test = 1

mid.save(filename_out)

exit(0)

# track = MidiTrack()
# mid.tracks.append(track)