import sys
sys.path.insert(0, '/Users/elliottevers/Documents/git-repos.nosync/music/src')
from message import messenger as mes
from utils import utils
import argparse
from filter import midi as filt_midi
from quantize import mesh
from postprocess import music_xml as postp_mxl
from i_o import exporter as io_exporter
from convert import music_xml as conv_mxl, midi as conv_mid, max as conv_max


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

    mesh_score = mesh.MeshScore()

    sample_rate = .0029

    df_melody_diff.index = df_melody_diff.index * sample_rate

    # TODO: add index s before quantizing

    tree_melody = mesh.MeshScore.get_interval_tree(
        df_melody_diff
    )

    mesh_score.set_tree(
        tree_melody,
        type='melody'
    )

    mesh_score.quantize(
        beatmap,
        s_beat_start,
        s_beat_end,
        columns=['melody']
    )

    score = postp_mxl.df_grans_to_score(
        mesh_score.data_quantized['melody'],
        parts=['melody']
    )

    exporter = io_exporter.Exporter()

    part_melody = postp_mxl.extract_part(
        score,
        'melody'
    )

    exporter.set_part(
        notes=conv_mxl.to_notes_live(
            part_melody,
            beatmap,
            s_beat_start,
            s_beat_end,
            tempo
        ),
        name_part='melody'
    )

    exporter.export(
        utils.get_file_json_comm()
    )

    messenger.message(['done', 'bang'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Export Melody')

    args = parser.parse_args()

    main(args)
