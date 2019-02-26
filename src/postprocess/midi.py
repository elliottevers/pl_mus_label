from mido import MidiFile, Message, MidiTrack
import pandas as pd
from subprocess import call as call_shell
import music21


def to_mid(score: music21.stream.Score, fp, channel_map={'bass': 2, 'chord': 3, 'melody': 4}) -> None:
    mf = music21.midi.translate.streamToMidiFile(score)
    # for part in score.parts:
    #     for name_part, channel in channel_map.items():
    #         mf = music21.midi.translate.streamToMidiFile(part)
    #
    #         for event in mf.tracks[0].events:
    #             event.channel = channel
    # TODO: this is sketchy, but music21 doesn't provice option to specify which part is mapped to which track
    def extract_track_map(score):
        track_map = []
        for part in score:
            track_map.append(part.partName)

        return track_map

    track_map = extract_track_map(score)

    for i, _ in enumerate(mf.tracks):
        for event in mf.tracks[i].events:
            event.channel = channel_map[track_map[i]]

    mf.open(fp, 'wb')
    mf.write()
    mf.close()

# dir_tracks = '/Users/elliottevers/Downloads/'
#
# filename_to_channel_mapping = {
#     'chords_and_bass.mid': 1,
#     'melody_unrepaired.mid': 2
# }
#
# filename_out = dir_tracks + 'merged_test.mid'
#
#
# def copy_track(track, channel, program=None):
#
#     track_new = MidiTrack()
#
#     if program:
#         track_new.append(Message('program_change', program=program, channel=channel))
#
#     for msg in track:
#         msg_copy = msg
#         if not msg.is_meta:
#             msg_copy.channel = channel
#         track_new.append(msg_copy)
#
#     return track_new
#
#
# file_resolution = MidiFile(dir_tracks + list(filename_to_channel_mapping)[0])
#
# file_out = MidiFile(ticks_per_beat=file_resolution.ticks_per_beat)
#
# for filename, channel in filename_to_channel_mapping.items():
#
#     file = MidiFile(dir_tracks + filename)
#
#     track = file.tracks[0]
#
#     track_new = copy_track(track=track, channel=channel - 1)
#
#     file_out.tracks.append(track_new)
#
#
# file_out.save(filename_out)
#
# name_program = '/Applications/MidiYodi 2018.1.app/'
#
# call_shell(['open', '-a', name_program, filename_out])
