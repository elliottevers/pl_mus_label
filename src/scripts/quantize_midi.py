import sys
sys.path.insert(0, '/Users/elliottevers/Documents/git-repos.nosync/tk_music_py/src')
from message import messenger as mes
import argparse
from utils import utils
from i_o import importer as io_importer, exporter as io_exporter
from convert import music_xml as convert_mxl, vamp as conv_vamp
from postprocess import music_xml as postp_mxl
from quantize import mesh
from preprocess import vamp as prep_vamp
import os


def main(args):

    use_warped = utils.b_use_warped()

    name_part = utils.parse_arg(args.name_part)

    beat_multiple_quantization = utils.parse_arg(args.beat_multiple)

    quarter_length_divisor = 1/float(beat_multiple_quantization)

    importer = io_importer.Importer(
        utils.get_file_json_comm()
    )

    importer.load([name_part])

    notes_live = importer.get_part(name_part)

    mode = 'polyphonic' if name_part == 'chord' else 'monophonic'

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

    stream = convert_mxl.live_to_stream(
        notes_live,
        beatmap=beatmap,
        s_beat_start=s_beat_start,
        s_beat_end=s_beat_end,
        tempo=tempo,
        mode=mode
    )

    # TODO: replace with logic in "granularize.py"
    if name_part == 'melody':

        data_melody = conv_vamp.to_data_melody(
            notes_live,
            offset_s_audio=0,
            duration_s_audio=utils.get_duration_s_audio(
                filename=os.path.join(
                    utils.get_dirname_audio_warped() if use_warped else utils.get_dirname_audio(),
                    utils._get_name_project_most_recent() + '.wav'
                )
            )
        )

        mesh_score = mesh.MeshScore()

        df_melody = prep_vamp.melody_to_df(
            (data_melody['vector'][0], data_melody['vector'][1]),
            index_type='s'
        )

        df_melody[df_melody['melody'] < 0] = 0

        melody_tree = mesh.MeshScore.get_interval_tree(
            df_melody
        )

        mesh_score.set_tree(
            melody_tree,
            type='melody'
        )

        mesh_score.quantize(
            beatmap,
            s_beat_start,
            s_beat_end,
            columns=['melody']
        )

        data_quantized_melody = mesh_score.data_quantized['melody']

        score = postp_mxl.df_grans_to_score(
            data_quantized_melody,
            parts=['melody']
        )

        stream = postp_mxl.extract_part(
            score,
            'melody'
        )
    else:
        stream.quantize(
            (quarter_length_divisor, ),
            inPlace=True
        )

    notes_live = convert_mxl.to_notes_live(
        stream,
        beatmap=beatmap,
        s_beat_start=s_beat_start,
        s_beat_end=s_beat_end,
        tempo=tempo,
        bypass_seconds=True
    )

    exporter = io_exporter.Exporter()

    exporter.set_part(notes_live, name_part)

    exporter.export(utils.get_file_json_comm())

    messenger.message(['done', 'bang'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Quantize Chords')

    parser.add_argument('--beat_multiple', help='e.g., if 4, quantize to the measure')

    parser.add_argument('--name_part', help='e.g., if 4, quantize to the measure')

    args = parser.parse_args()

    main(args)
