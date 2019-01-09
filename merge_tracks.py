from mido import MidiFile, Message, MidiTrack
from subprocess import call as call_shell

dir_tracks = '/Users/elliottevers/Downloads/'

filename_to_channel_mapping = {
    'chords_and_bass.mid': 1,
    'melody_unrepaired.mid': 2
}

filename_out = dir_tracks + 'merged_test.mid'


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


file_resolution = MidiFile(dir_tracks + list(filename_to_channel_mapping)[0])

file_out = MidiFile(ticks_per_beat=file_resolution.ticks_per_beat)

for filename, channel in filename_to_channel_mapping.items():

    file = MidiFile(dir_tracks + filename)

    track = file.tracks[0]

    track_new = copy_track(track=track, channel=channel - 1)

    file_out.tracks.append(track_new)


file_out.save(filename_out)

name_program = '/Applications/MidiYodi 2018.1.app/'

call_shell(['open', '-a', name_program, filename_out])
