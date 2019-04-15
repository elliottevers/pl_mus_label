from information_retrieval import extraction as ir
from message import messenger as mes
import argparse
import librosa
from preprocess import vamp as prep_vamp
from postprocess import music_xml as postp_mxl
from music import song
from utils import utils
import os
from convert import music_xml as convert_mxl
from i_o import exporter as io_exporter
from utils import musix_xml as utils_mxl


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

    beat_start_marker, beat_end_marker, beat_loop_bracket_lower, beat_loop_bracket_upper, length_beats, beatmap = utils.get_tuple_beats(
        os.path.join(
            utils.get_dirname_beat(),
            utils._get_name_project_most_recent() + '.pkl'
        )
    )

    messenger.message(['length_beats', str(length_beats)])

    s_beat_start = (beat_start_marker / length_beats) * duration_s_audio

    s_beat_end = (beat_end_marker / (length_beats)) * duration_s_audio

    # NB: chords from raw audio
    data_segments = ir.extract_segments(
        os.path.join(
            utils.get_dirname_audio_warped(),
            utils._get_name_project_most_recent() + '.wav'
        )
    )

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
        beat_start_marker,  # transitioning indices here
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
        ''.join(
            [
                utils._get_name_project_most_recent(),
                '.pkl'
            ]
        )
    )

    utils_mxl.freeze_stream(
        stream_segment,
        filename_pickle
    )

    notes_live = convert_mxl.to_notes_live(
        stream_segment
    )

    exporter = io_exporter.Exporter()

    exporter.set_part(notes_live, 'segment')

    exporter.export(utils.get_file_json_comm())

    messenger.message(['done'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract Segments')

    args = parser.parse_args()

    main(args)
