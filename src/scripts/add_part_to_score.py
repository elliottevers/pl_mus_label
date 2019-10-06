import sys
sys.path.insert(0, '/Users/elliottevers/Documents/git-repos.nosync/music/src')
from message import messenger as mes
import argparse
import os
from utils import utils
from i_o import importer as io_importer
from postprocess import live as postp_live
from utils import musix_xml as utils_mxl
from convert import music_xml as conv_mxl


def main(args):

    name_part = args.name_part.replace("\"", '')

    importer = io_importer.Importer(
        utils.get_file_json_comm()
    )

    importer.load([name_part])

    notes_live = postp_live.filter_empty(importer.get_part(name_part))

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

    stream = conv_mxl.live_to_stream(
        notes_live,
        beatmap=beatmap,
        s_beat_start=s_beat_start,
        s_beat_end=s_beat_end,
        tempo=tempo,
        mode=mode
    )

    utils.create_dir_score()

    utils.create_dir_part(name_part)

    filename_pickle = os.path.join(
        utils.get_dirname_score(),
        name_part,
        ''.join(
            [
                utils._get_name_project_most_recent(),
                '.pkl'
            ]
        )
    )

    utils_mxl.freeze_stream(
        stream,
        filename_pickle
    )

    messenger = mes.Messenger()

    messenger.message(['done', 'bang'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Quantize Chords')

    parser.add_argument('--name_part', help='e.g., if 4, quantize to the measure')

    args = parser.parse_args()

    main(args)
