from mido import MidiFile

file_midi_master_raw = MidiFile('lodi_master_raw.mid')

filename_overlay = 'lodi_master_raw_overlay.mid'

midi_file_vocals = MidiFile('lodi_vocals.mid')

track_vocals = midi_file_vocals.tracks[0]

file_midi_master_raw.tracks.append(track_vocals)

file_midi_master_raw.save(filename_overlay)

test = 1