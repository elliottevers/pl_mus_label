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
from convert import music_xml as conv_mxl

# TODO: get the filepath of the cache module
# filename_chords_to_live = utils.get_path_cache(utils.FILE_CHORD_TO_LIVE)

dir_projects = os.path.dirname('/Users/elliottevers/Documents/DocumentsSymlinked/git-repos.nosync/tk_music_projects/')

# TODO: replace

# beatmap_manual = np.linspace(
#     0,
#     float(148.66997732426304),
#     int(297) - int(1) + 1
# )


def main(args):
    messenger = mes.Messenger()
    #
    # messenger.message(['running'])

    # filename_wav = utils.FILE_WAV_DOWNLOADED

    filename_wav = os.path.join(
        utils.get_dirname_audio_warped(),
        utils._get_name_project_most_recent() + '.wav'
    )

    y, sr = librosa.load(
        filename_wav
    )

    duration_s_audio = librosa.get_duration(
        y=y,
        sr=sr
    )

    beat_start, beat_end, length_beats, beatmap = utils.get_tuple_beats(
        os.path.join(
            utils.get_dirname_beat(),
            utils._get_name_project_most_recent() + '.pkl'
        )
    )

    # duration_s_audio_warped = 148.670

    # length of Ableton live track in beats

    # beats_length_track_live = args.beats_length_track_live

    # beat_start = args.beat_start

    # beat_start = (9 - 1) * 4 + 1  # 1  # args.beat_start

    # beat_end = args.beat_end

    # beat_end = (13 - 1) * 4 + 1  # 297  # args.beat_end

    # beats_length_track_live = args.beats_length_track_live

    # beats_length_track_live = 74 * 4 + 1

    s_beat_start = (beat_start / length_beats) * duration_s_audio

    s_beat_end = (beat_end / (length_beats)) * duration_s_audio

    # NB: chords from raw audio
    data_chords = ir.extract_chords(
        os.path.join(
            utils.get_dirname_audio_warped(),
            utils._get_name_project_most_recent() + '.wav'
        )
    )

    # TODO: implement when doing caching
    # utils.save(
    #     'chord',
    #     data_chords
    # )

    mesh_song = song.MeshSong()

    non_empty_chords = vamp_filter.vamp_filter_non_chords(
        data_chords
    )

    # TODO: refactor, this is slow
    events_chords: Dict[float, music21.chord.Chord] = vamp_convert.vamp_chord_to_dict(
        non_empty_chords
    )

    df_chords = prep_vamp.chords_to_df(
        events_chords
    )

    # TODO: put somewhere else
    # df_upper_voicings = postp_mxl.extract_upper_voices(
    #     df_chords
    # )

    chord_tree = song.MeshSong.get_interval_tree(
        df_chords
    )

    mesh_song.set_tree(
        chord_tree,
        type='chord'
    )

    # data_beats = ir.extract_beats(
    #     filepath_beat,
    #     from_cache=True
    # )
    #
    # beatmap = prep_vamp.extract_beatmap(
    #     data_beats
    # )

    # beatmap = utils.load_pickle(
    #     filepath_beat
    # )

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

    part_chord = postp_mxl.extract_part(
        score,
        'chord'
    )

    utils.create_dir_score()

    utils.create_dir_chord()

    filename_pickle = os.path.join(
        utils.get_dirname_score(),
        'chord',
        ''.join([utils._get_name_project_most_recent(), '.pkl'])
    )

    postp_mxl.freeze_stream(
        part_chord,
        filename_pickle
    )

    json_live = {}

    # TODO: put in module
    if False:
        for part in score:
            json_live[part.id] = {'notes': []}
            notes_final = []

            for obj in part:
                notes = conv_mxl.struct_to_notes_live(obj, part.id)
                # TODO: filter lowest note here to extract upper voicings
                for note_live in notes:
                    notes_final.append(note_live.encode())

            json_live[part.id]['notes'].append(' '.join(['notes', str(len(notes_final))]))

            for note_final in notes_final:
                json_live[part.id]['notes'].append(note_final)

            json_live[part.id]['notes'].append(' '.join(['notes', 'done']))

        utils.to_json_live(
            json_live,
            filename_chords_to_live=os.path.join(dir_projects, 'json_live.json')
        )

    messenger.message(['done'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract Chords')

    # parser.add_argument('beats_length_track_live', help='length of track in Live')
    #
    # parser.add_argument('beat_start', help='first beat in Live')
    #
    # parser.add_argument('beat_end', help='last beat in Live')

    args = parser.parse_args()

    main(args)
