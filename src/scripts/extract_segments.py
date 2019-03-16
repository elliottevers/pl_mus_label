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
import os


dir_projects = os.path.dirname('/Users/elliottevers/Documents/DocumentsSymlinked/git-repos.nosync/tk_music_projects/')


def main(args):

    messenger = mes.Messenger()

    y, sr = librosa.load(
        os.path.join(
            utils.get_dirname_audio_warped(),
            utils._get_name_project_most_recent() + '.wav'
        )
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

    s_beat_start = (beat_start / length_beats) * duration_s_audio

    s_beat_end = (beat_end / (length_beats)) * duration_s_audio

    # NB: chords from raw audio
    data_segments = ir.extract_segments(
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

    df_segments = prep_vamp.segments_to_df(
        data_segments
    )

    segment_tree = song.MeshSong.get_interval_tree(
        df_segments
    )

    mesh_song.set_tree(
        segment_tree,
        type='segment'
    )

    mesh_song.quantize(
        beatmap,
        s_beat_start,
        s_beat_end,
        beat_start - 1,  # transitioning indices here
        columns=['segment']
    )

    data_quantized_chords = mesh_song.data_quantized['segment']

    # print(data_quantized_chords[data_quantized_chords.index.get_level_values(1) == 16.574693417907703])
    # print(data_quantized_chords[data_quantized_chords.index.get_level_values(1) == 24.61090840840841])

    score = postp_mxl.df_grans_to_score(
        data_quantized_chords,
        parts=['segment']
    )

    messenger.message(['done'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract Segments')

    # parser.add_argument('beats_length_track_live', help='length of track in Live')
    #
    # parser.add_argument('beat_start', help='first beat in Live')
    #
    # parser.add_argument('beat_end', help='last beat in Live')

    args = parser.parse_args()

    main(args)
