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

    score = postp_mxl.df_grans_to_score(
        data_quantized_chords,
        parts=['segment']
    )

    stream_segment = postp_mxl.extract_part(
        score,
        'segment'
    )

    utils.create_dir_score()

    utils.create_dir_segment()

    filename_pickle = os.path.join(
        utils.get_dirname_score(),
        'segment',
        ''.join([utils._get_name_project_most_recent(), '.pkl'])
    )

    postp_mxl.freeze_stream(
        stream_segment,
        filename_pickle
    )

    stream_segment_thawed = postp_mxl.thaw_stream(
        filename_pickle
    )

    messenger.message(['done'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract Segments')

    args = parser.parse_args()

    main(args)
