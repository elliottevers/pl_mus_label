from message import messenger as mes
from utils import utils
import argparse
from filter import midi as filt_midi
from music import song
import os
from postprocess import music_xml as postp_mxl
from i_o import exporter as io_exporter
from convert import music_xml as conv_mxl, midi as conv_mid, max as conv_max


def main(args):

    messenger = mes.Messenger()

    beat_start_marker, beat_end_marker, beat_loop_bracket_lower, beat_loop_bracket_upper, length_beats, beatmap = utils.get_tuple_beats(
        os.path.join(
            utils.get_dirname_beat(),
            utils._get_name_project_most_recent() + '.pkl'
        )
    )

    messenger.message(['length_beats', str(length_beats)])

    df = conv_max.from_coll(
        conv_max.file_ts_coll
    )

    df = conv_mid.hz_to_mid(
        df.rename(
            columns={'signal': 'melody'}
        )
    )

    df_melody_diff = filt_midi.to_diff(
        df,
        'melody'
    )

    mesh_song = song.MeshSong()

    sample_rate = .0029

    df_melody_diff.index = df_melody_diff.index * sample_rate

    # TODO: add index s before quantizing

    tree_melody = song.MeshSong.get_interval_tree(
        df_melody_diff
    )

    mesh_song.set_tree(
        tree_melody,
        type='melody'
    )

    mesh_song.quantize(
        beatmap,
        beat_start_marker,
        beat_end_marker,
        0,
        columns=['melody']
    )

    score = postp_mxl.df_grans_to_score(
        mesh_song.data_quantized['melody'],
        parts=['melody']
    )

    exporter = io_exporter.Exporter()

    part_melody = postp_mxl.extract_part(
        score,
        'melody'
    )

    exporter.set_part(
        conv_mxl.to_notes_live(part_melody),
        'melody'
    )

    exporter.export(
        utils.get_file_json_comm()
    )

    messenger.message(['done', 'bang'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Export Melody')

    args = parser.parse_args()

    main(args)
