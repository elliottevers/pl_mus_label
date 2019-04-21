from message import messenger as mes
import argparse
from utils import utils
from i_o import importer as io_importer, exporter as io_exporter
from convert import music_xml as convert_mxl, vamp as conv_vamp
from postprocess import music_xml as postp_mxl
from quantize import mesh
from preprocess import vamp as prep_vamp
from filter import midi as filt_midi
from convert import live as conv_live
import os


def main(args):

    name_part = utils.parse_arg(args.name_part)

    importer = io_importer.Importer(
        utils.get_file_json_comm()
    )

    importer.load([name_part])

    notes_live = importer.get_part(name_part)

    (
        s_beat_start,
        s_beat_end,
        tempo,
        beat_start,
        beat_end,
        length_beats,
        beatmap
    ) = utils.get_tuple_beats()

    data_monophonic = conv_vamp.to_data_monophonic(
        notes_live,
        offset_s_audio=0,
        duration_s_audio=utils.get_duration_s_audio(
            filename=os.path.join(
                utils.get_dirname_audio_warped() if utils.b_use_warped() else utils.get_dirname_audio(),
                utils._get_name_project_most_recent() + '.wav'
            )
        ),
        beatmap=beatmap,
        sample_rate=float(1/100)
    )

    mesh_song = mesh.MeshScore()

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

    interval_tree = mesh.MeshScore.get_interval_tree(
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
        0,
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
        stream,
        beatmap,
        s_beat_start,
        s_beat_end,
        tempo
    )

    exporter = io_exporter.Exporter()

    exporter.set_part(notes_live, name_part)

    exporter.export(utils.get_file_json_comm())

    messenger = mes.Messenger()

    messenger.message(['done', 'bang'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Make part monophonic')

    parser.add_argument('--name_part', help='name of part, e.g., melody')

    args = parser.parse_args()

    main(args)
