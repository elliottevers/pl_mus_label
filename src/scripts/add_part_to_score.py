from message import messenger as mes
import argparse
import os
from utils import utils
from i_o import importer as io_importer
from postprocess import music_xml as postp_mxl
from utils import musix_xml as utils_mxl


def main(args):

    name_part = args.name_part.replace("\"", '')

    importer = io_importer.Importer(
        utils.get_file_json_comm()
    )

    importer.load([name_part])

    notes_live = importer.get_part(name_part)

    notes_live = list(filter(lambda note: note.beats_duration > 0, notes_live))

    # convert ableton live notes to stream

    mode = 'polyphonic' if name_part == 'chord' else 'monophonic'

    stream = postp_mxl.live_to_stream(
        notes_live,
        mode
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
