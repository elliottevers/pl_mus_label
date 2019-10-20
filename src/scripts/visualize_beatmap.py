import sys
sys.path.insert(0, '/Users/elliottevers/Documents/git-repos.nosync/tk_music_py/src')
from message import messenger as mes
import argparse
from preprocess import vamp as prep_vamp
from postprocess import music_xml as postp_mxl
from quantize import mesh
from utils import utils
from convert import music_xml as convert_mxl
from i_o import exporter as io_exporter


def main(args):

    (
        s_beat_start,
        s_beat_end,
        tempo,
        beat_start,
        beat_end,
        length_beats,
        beatmap
    ) = utils.get_tuple_beats()

    messenger = mes.Messenger()

    messenger.message(['length_beats', str(length_beats)])

    mesh_score = mesh.MeshScore()

    ts_beatmap = prep_vamp.beatmap_to_ts(
        beatmap
    )

    df_beatmap = prep_vamp.ts_beatmap_to_df(
        ts_beatmap
    )

    beatmap_tree = mesh.MeshScore.get_interval_tree(
        df_beatmap,
        diff=False,
        preserve_struct=True
    )

    mesh_score.set_tree(
        beatmap_tree,
        type='beatmap'
    )

    mesh_score.quantize(
        beatmap,
        s_beat_start,
        s_beat_end,
        columns=['beatmap']
    )

    data_quantized_beats = mesh_score.data_quantized['beatmap']

    score = postp_mxl.df_grans_to_score(
        data_quantized_beats,
        parts=['beatmap'],
        type_equality='absolute'
    )

    stream_beatmap = postp_mxl.extract_part(
        score,
        'beatmap'
    )

    notes_live = convert_mxl.to_notes_live(
        stream_beatmap,
        beatmap,
        s_beat_start,
        s_beat_end,
        tempo
    )

    exporter = io_exporter.Exporter()

    exporter.set_part(notes_live, 'beatmap')

    exporter.export(utils.get_file_json_comm())

    messenger.message(['done', 'bang'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract Beatmap')

    args = parser.parse_args()

    main(args)
