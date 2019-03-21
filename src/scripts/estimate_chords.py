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
from utils import utils, musix_xml as utils_mxl
import numpy as np
import os
from information_retrieval import extraction
from live import note as nl
from convert import music_xml as conv_mxl


dir_projects = os.path.dirname('/Users/elliottevers/Documents/DocumentsSymlinked/git-repos.nosync/tk_music_projects/')


def main(args):
    messenger = mes.Messenger()

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

    beat_start_marker, beat_end_marker, beat_loop_bracket_lower, beat_loop_bracket_upper, length_beats, beatmap = utils.get_tuple_beats(
        os.path.join(
            utils.get_dirname_beat(),
            utils._get_name_project_most_recent() + '.pkl'
        )
    )

    s_beat_start = (beat_start_marker / length_beats) * duration_s_audio

    s_beat_end = (beat_end_marker / length_beats) * duration_s_audio

    # NB: chords from raw audio
    data_chords = ir.extract_chords(
        os.path.join(
            utils.get_dirname_audio_warped(),
            utils._get_name_project_most_recent() + '.wav'
        )
    )

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

    chord_tree = song.MeshSong.get_interval_tree(
        df_chords
    )

    mesh_song.set_tree(
        chord_tree,
        type='chord'
    )

    mesh_song.set_tree(
        chord_tree,
        type='chord'
    )

    mesh_song.quantize(
        beatmap,
        s_beat_start,
        s_beat_end,
        beat_start_marker,  # transitioning indices here - beat_start_marker - 1
        columns=['chord']
    )

    data_quantized_chords = mesh_song.data_quantized['chord']

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

    utils_mxl.freeze_stream(
        part_chord,
        filename_pickle
    )

    # TODO: put in module
    if False:
        json_live = {}

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
