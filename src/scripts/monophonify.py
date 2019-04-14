from message import messenger as mes
import argparse
from utils import utils
from i_o import importer as io_importer, exporter as io_exporter
from convert import music_xml as convert_mxl, vamp as conv_vamp
from postprocess import music_xml as postp_mxl
from music import song
import os
import librosa
from preprocess import vamp as prep_vamp
from filter import midi as filt_midi
from convert import live as conv_live


def main(args):

    name_part = args.name_part.replace("\"", '')

    importer = io_importer.Importer(
        utils.get_file_json_comm()
    )

    importer.load([name_part])

    notes_live = importer.get_part(name_part)

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

    s_beat_start = (beat_start_marker / length_beats) * duration_s_audio

    s_beat_end = (beat_end_marker / length_beats) * duration_s_audio

    data_monophonic = conv_vamp.to_data_monophonic(
        notes_live,
        offset_s_audio=0,
        duration_s_audio=duration_s_audio,
        beatmap=beatmap,
        sample_rate=float(1/100)
    )

    mesh_song = song.MeshSong()

    df = prep_vamp.monophony_to_df(
        (data_monophonic['vector'][0], data_monophonic['vector'][1]),
        name_part=name_part,
        index_type='s'
    )

    df[df[name_part] < 0] = 0

    df_diff = filt_midi.to_diff(
        df,
        name_part,
        sample_rate=float(1/100)
    )

    interval_tree = song.MeshSong.get_interval_tree(
        df_diff
    )

    mesh_song.set_tree(
        interval_tree,
        type=name_part
    )

    mesh_song.quantize(
        beatmap,
        s_beat_start,
        s_beat_end,
        beat_start_marker,
        columns=[name_part]
    )

    data_quantized = conv_live.with_index_live(
        mesh_song.data_quantized[name_part]
    )

    score = postp_mxl.df_grans_to_score(
        data_quantized,
        parts=[name_part]
    )

    stream = postp_mxl.extract_part(
        score,
        name_part
    )

    notes_live = convert_mxl.to_notes_live(
        stream
    )

    exporter = io_exporter.Exporter()

    exporter.set_part(notes_live, name_part)

    exporter.export(utils.get_file_json_comm())

    messenger = mes.Messenger()

    messenger.message(['done'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Make part monophonic')

    parser.add_argument('--name_part', help='name of part, e.g., melody')

    args = parser.parse_args()

    main(args)
