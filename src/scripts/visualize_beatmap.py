from message import messenger as mes
import argparse
from preprocess import vamp as prep_vamp
from postprocess import music_xml as postp_mxl
from music import song
from utils import utils
from convert import music_xml as convert_mxl
from i_o import exporter as io_exporter


def main(args):

    use_warped = utils.b_use_warped()

    (
        beat_start_marker,
        beat_end_marker,
        s_beat_start,
        s_beat_end,
        length_beats,
        duration_s_audio,
        beatmap
    ) = utils.get_grid_beats(
        use_warped=use_warped
    )

    messenger = mes.Messenger()

    messenger.message(['length_beats', str(length_beats)])

    mesh_song = song.MeshSong()

    df_beatmap = prep_vamp.beatmap_to_df(
        beatmap
    )

    beatmap_tree = song.MeshSong.get_interval_tree(
        df_beatmap
    )

    mesh_song.set_tree(
        beatmap_tree,
        type='beatmap'
    )

    mesh_song.quantize(
        beatmap,
        s_beat_start,
        s_beat_end,
        0,
        columns=['beatmap']
    )

    data_quantized_beats = mesh_song.data_quantized['beatmap']

    score = postp_mxl.df_grans_to_score(
        data_quantized_beats,
        parts=['beatmap']
    )

    stream_beatmap = postp_mxl.extract_part(
        score,
        'beatmap'
    )

    notes_live = convert_mxl.to_notes_live(
        stream_beatmap
    )

    exporter = io_exporter.Exporter()

    exporter.set_part(notes_live, 'beatmap')

    exporter.export(utils.get_file_json_comm())

    messenger.message(['done', 'bang'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract Segments')

    parser.add_argument('--representation', help='either symbolic or numeric')

    args = parser.parse_args()

    main(args)
