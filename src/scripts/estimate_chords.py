from information_retrieval import extraction as ir
from message import messenger as mes
import argparse
import librosa
from typing import List, Dict, Any
from filter import vamp as vamp_filter
from convert import vamp as vamp_convert
from preprocess import vamp as prep_vamp
from postprocess import music_xml as postp_mxl
from music import song
import music21
import json
from utils import utils
import numpy as np
import os
from information_retrieval import extraction
from live import note as nl

# TODO: get the filepath of the cache module
# filename_chords_to_live = utils.get_path_cache(utils.FILE_CHORD_TO_LIVE)


# TODO: replace

beatmap_manual = np.linspace(
    0,
    float(148.66997732426304),
    int(297) - int(1) + 1
)


# add live index (beats)


def main(args):
    messenger = mes.Messenger()
    #
    # messenger.message(['running'])

    # filename_wav = utils.FILE_WAV_DOWNLOADED

    filename_wav = os.path.join(
        extraction._get_dirname_audio_warped(),
        extraction._get_name_project_most_recent() + '.wav'
    )

    y, sr = librosa.load(
        filename_wav
    )

    duration_s_audio = librosa.get_duration(
        y=y,
        sr=sr
    )

    duration_s_audio = 148.670
    # length of Ableton live track in beats

    # beats_length_track_live = args.beats_length_track_live

    # beat start

    beat_start = (9 - 1) * 4 + 1  # 1  # args.beat_start

    # beat end

    beat_end = (13 - 1) * 4 + 1  # 297  # args.beat_end

    # length of wav file in s
    # y, sr = librosa.load(filename_wav)
    #
    # duration_s_audio = librosa.get_duration(y=y, sr=sr)

    beats_length_track_live = 74 * 4 + 1

    s_beat_start = (beat_start / beats_length_track_live) * duration_s_audio

    s_beat_end = (beat_end / (beats_length_track_live)) * duration_s_audio

    data_chords = ir.extract_chords(
        filename_wav
    )

    mesh_song = song.MeshSong()

    non_empty_chords = vamp_filter.vamp_filter_non_chords(
        data_chords
    )

    events_chords: Dict[float, music21.chord.Chord] = vamp_convert.vamp_chord_to_dict(
        non_empty_chords
    )

    df_chords = prep_vamp.chords_to_df(
        events_chords
    )

    df_upper_voicings = postp_mxl.extract_upper_voices(
        df_chords
    )

    chord_tree = song.MeshSong.get_interval_tree(
        df_upper_voicings
    )

    mesh_song.set_tree(
        chord_tree,
        type='chord'
    )


    # s_to_label_chords: List[Dict[float, Any]] = data_chords
    #
    # non_empty_chords = vamp_filter.vamp_filter_non_chords(
    #     s_to_label_chords
    # )
    #
    # events_chords: Dict[float, music21.chord.Chord] = vamp_convert.vamp_chord_to_dict(
    #     non_empty_chords
    # )
    #
    # df_chords = prep_vamp.chords_to_df(
    #     events_chords
    # )
    #
    # df_upper_voicings = postp_mxl.extract_upper_voices(
    #     df_chords
    # )
    #
    # chord_tree = song.MeshSong.get_interval_tree(
    #     df_upper_voicings
    # )
    #





    # mesh_song = song.MeshSong()
    #
    # data_beats = ir.extract_beats(
    #     filename_wav,
    #     from_cache=True
    # )
    #
    # beatmap = prep_vamp.extract_beatmap(
    #     data_beats
    # )

    beatmap = beatmap_manual

    mesh_song.set_tree(
        chord_tree,
        type='chord'
    )

    mesh_song.quantize(
        beatmap,
        s_beat_start,
        s_beat_end,
        beat_start - 1,  # transitioning indices here
        columns=['chord']
    )

    data_quantized_chords = mesh_song.data_quantized['chord']

    # print(data_quantized_chords[data_quantized_chords.index.get_level_values(1) == 16.574693417907703])
    # print(data_quantized_chords[data_quantized_chords.index.get_level_values(1) == 24.61090840840841])

    score = postp_mxl.df_grans_to_score(
        data_quantized_chords,
        parts=['chord']
    )

    json_live = {}

    def struct_to_notes_live(struct_21, name_part):

        try:
            if struct_21.name == 'rest':
                return []
        except AttributeError:
            pass

        notes = []

        if name_part == 'melody':
            # if not object > 0:
            #     struct_score = note.Rest()
            # else:
            #     struct_score = note.Note(
            #         pitch=pitch.Pitch(
            #             midi=int(object)
            #         )
            #     )
            testing = 1
        elif name_part == 'chord':
            beats_offset = float(struct_21.offset)
            beats_duration = float(struct_21.duration.quarterLength)
            velocity = 90
            muted = 0

            for pitch in struct_21.pitches:
                notes.append(
                    nl.NoteLive.parse(
                        [pitch.midi, beats_offset, beats_duration, velocity, muted]
                    )
                )

        elif name_part == 'bass':
            # struct_score = note.Note(
            #     pitch=object
            # )
            testing = 1
        elif name_part == 'segment':
            # struct_score = note.Note(
            #     pitch=pitch.Pitch(
            #         midi=60
            #     )
            # )
            testing = 1
        else:
            raise 'part ' + name_part + ' not able to be converted to Live'

        return notes

    for part in score:
        json_live[part.id] = {'notes': []}
        for obj in part:
            # length_beats = float(obj.duration.quarterLength)
            # offset_beats = obj.offset
            notes = struct_to_notes_live(obj, part.id)
            for note_live in notes:
                json_live[part.id]['notes'].append(note_live.encode())

    # print(json_live)

    exit(0)

    # # index beat, index ms audio file, index beat live audio track
    # df_with_live_audio_index = song.MeshSong.add_live_index(
    #     mesh_song.data_quantized,
    #     beat_start_live=beat_start,
    #     beat_end_live=beat_end,
    #     beats_length_track_live=beats_length_track_live
    # )
    #
    # # TODO: save Live JSON for chords synced with audio track in Live
    #
    # dict_write_json_live = song.MeshSong.to_json_live(
    #     df_with_live_audio_index,
    #     columns=['chord']
    # )
    #
    # utils.to_json_live(
    #     dict_write_json_live,
    #     filename_chords_to_live=filename_chords_to_live
    # )
    #
    # score_chords = postp_mxl.df_grans_to_score(
    #     df_with_live_audio_index,
    #     parts=['chord']
    # )
    #
    # postp_mxl.freeze_stream(
    #     stream=score_chords,
    #     filepath=utils.CHORD_SCORE
    # )

    # messenger.message(['done'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract Chords')

    # parser.add_argument('beats_length_track_live', help='length of track in Live')
    #
    # parser.add_argument('beat_start', help='first beat in Live')
    #
    # parser.add_argument('beat_end', help='last beat in Live')

    args = parser.parse_args()

    main(args)
