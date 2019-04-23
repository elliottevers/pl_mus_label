from information_retrieval import extraction as ir
from message import messenger as mes
import argparse
from typing import Dict
from filter import vamp as vamp_filter
from convert import vamp as vamp_convert
from preprocess import vamp as prep_vamp
from postprocess import music_xml as postp_mxl
from convert import music_xml as convert_mxl
from i_o import exporter as io_exporter
from quantize import mesh
import music21
from utils import utils, musix_xml as utils_mxl
import os


def main(args):

    messenger = mes.Messenger()

    (
        s_beat_start,
        s_beat_end,
        tempo,
        beat_start,
        beat_end,
        length_beats,
        beatmap
    ) = utils.get_tuple_beats()

    messenger.message(['length_beats', str(length_beats)])

    data_chords = ir.extract_chords(
        os.path.join(
            utils.get_dirname_audio_warped() if utils.b_use_warped() else utils.get_dirname_audio(),
            utils._get_name_project_most_recent() + '.wav'
        )
    )

    mesh_score = mesh.MeshScore()

    non_empty_chords = vamp_filter.vamp_filter_non_chords(
        data_chords
    )

    # TODO: refactor, this is slow
    events_chords: Dict[float, music21.chord.Chord] = vamp_convert.vamp_chord_to_dict(
        non_empty_chords
    )

    df_chords = prep_vamp.chords_to_df(
        events_chords
    )

    chord_tree = mesh.MeshScore.get_interval_tree(
        df_chords,
        diff=False
    )

    mesh_score.set_tree(
        chord_tree,
        type='chord'
    )

    mesh_score.set_tree(
        chord_tree,
        type='chord'
    )

    mesh_score.quantize(
        beatmap,
        s_beat_start,
        s_beat_end,
        columns=['chord']
    )

    data_quantized_chords = mesh_score.data_quantized['chord']

    score = postp_mxl.df_grans_to_score(
        data_quantized_chords,
        parts=['chord']
    )

    part_chord = postp_mxl.extract_part(
        score,
        'chord'
    )

    part_chord = postp_mxl.force_texture(
        part_chord,
        num_voices=4
    )

    utils.create_dir_score()

    utils.create_dir_chord()

    filename_pickle = os.path.join(
        utils.get_dirname_score(),
        'chord',
        ''.join([utils._get_name_project_most_recent(), '.pkl'])
    )

    utils_mxl.freeze_stream(
        part_chord,
        filename_pickle
    )

    notes_live = convert_mxl.to_notes_live(
        part_chord,
        beatmap=beatmap,
        s_beat_start=s_beat_start,
        s_beat_end=s_beat_end,
        tempo=tempo
    )

    exporter = io_exporter.Exporter()

    exporter.set_part(notes_live, 'chord')

    exporter.export(utils.get_file_json_comm())

    messenger.message(['done', 'bang'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract Chords')

    # parser.add_argument('beats_length_track_live', help='length of track in Live')
    #
    # parser.add_argument('beat_start', help='first beat in Live')
    #
    # parser.add_argument('beat_end', help='last beat in Live')

    args = parser.parse_args()

    main(args)
