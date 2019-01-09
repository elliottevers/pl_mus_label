from mido import MidiFile, Message, MidiTrack
from subprocess import call as call_shell


# dir_tracks = '/Users/elliottevers/Documents/tracks/export/ableton/'
dir_tracks = '/Users/elliottevers/Documents/tracks/export/ableton/biab_sync/'
filename_bass = dir_tracks + 'bass.mid'
# filename_melody = dir_tracks + 'melody.mid'
filename_chords = dir_tracks + 'chords.mid'
# filename_segments = dir_tracks + 'segments.mid'
# filename_keys = dir_tracks + 'keys.mid'

filename_out = dir_tracks + 'merged.mid'

channel_bass = 1
channel_chords = 2
# channel_melody = 3
# channel_segments = 4
# channel_keys = 5

# file_melody = MidiFile(filename_melody)

file_bass = MidiFile(filename_bass)

file_chords = MidiFile(filename_chords)

# file_segments = MidiFile(filename_segments)

# file_keys = MidiFile(filename_keys)

# melody = file_melody.tracks[0]

bass = file_bass.tracks[0]

chords = file_chords.tracks[0]

# segments = file_segments.tracks[0]

# keys = file_keys.tracks[0]


def copy_track(track, channel, program=None):

    track_new = MidiTrack()

    if program:
        track_new.append(Message('program_change', program=program, channel=channel))

    for msg in track:
        msg_copy = msg
        if not msg.is_meta:
            msg_copy.channel = channel
        track_new.append(msg_copy)

    return track_new


# melody_new = copy_track(track=melody, channel=channel_melody)
bass_new = copy_track(track=bass, channel=channel_bass)
chords_new = copy_track(track=chords, channel=channel_chords)
# segments_new = copy_track(track=segments, channel=channel_segments, program=119)
# keys_new = copy_track(track=keys, channel=channel_keys)


file_out = MidiFile(ticks_per_beat=file_chords.ticks_per_beat)

# file_out.tracks.append(melody_new)

file_out.tracks.append(bass_new)

file_out.tracks.append(chords_new)

# file_out.tracks.append(segments_new)

# file_out.tracks.append(keys_new)


# mid = MidiFile()
# track = MidiTrack()
# mid.tracks.append(track)
#
# track.append(Message('program_change', program=12, time=0))
# track.append(Message('note_on', note=64, velocity=64, time=32))
# track.append(Message('note_off', note=64, velocity=127, time=32))
#
# mid.save(filename_out)


file_out.save(filename_out)

# name_program = '/Applications/MuseScore 2.app/Contents/MacOS//mscore'  # '/Applications/MidiYodi 2018.1.app/'

name_program = '/Applications/MidiYodi 2018.1.app/'

call_shell(['open', '-a', name_program, filename_out])
