import sys
sys.path.insert(0, '/Users/elliottevers/Documents/DocumentsSymlinked/git-repos.nosync/music/src')
from message import messenger as mes
import argparse
from utils import utils
import os
from convert import music_xml as convert_mxl
from i_o import exporter as io_exporter
from analysis_discrete import music_xml as analysis_mxl
from utils import musix_xml as utils_mxl


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

    filename_pickle = os.path.join(
        utils.get_dirname_score(),
        'chord',
        ''.join([utils._get_name_project_most_recent(), '.pkl'])
    )

    part_chord_thawed = utils_mxl.thaw_stream(
        filename_pickle
    )

    part_key_centers = analysis_mxl.get_key_center_estimates(
        part_chord_thawed
    )

    utils.create_dir_score()

    utils.create_dir_key_center()

    filename_pickle = os.path.join(
        utils.get_dirname_score(),
        'key_center',
        ''.join([utils._get_name_project_most_recent(), '.pkl'])
    )

    ################ TODO: remove

    # filename_part = os.path.join(
    #     utils.get_dirname_score(),
    #     'key_center',
    #     utils._get_name_project_most_recent() + '.pkl'
    # )
    #
    # part_key_centers = utils_mxl.thaw_stream(
    #     filename_part
    # )

    ###############

    utils_mxl.freeze_stream(
        part_key_centers,
        filename_pickle
    )

    notes_live = convert_mxl.to_notes_live(
        part_key_centers,
        beatmap=beatmap,
        s_beat_start=s_beat_start,
        s_beat_end=s_beat_end,
        tempo=tempo
    )

    exporter = io_exporter.Exporter()

    exporter.set_part(notes_live, 'key_center')

    exporter.export(utils.get_file_json_comm())

    messenger.message(['done', 'bang'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract Segments')

    args = parser.parse_args()

    main(args)
