from message import messenger as mes
import argparse
from utils import utils
import os
from convert import music_xml as convert_mxl
from i_o import exporter as io_exporter
from utils import musix_xml as utils_mxl
from postprocess import music_xml as postp_mxl


def main(args):

    messenger = mes.Messenger()

    _, _, _, _, length_beats, _ = utils.get_tuple_beats(
        os.path.join(
            utils.get_dirname_beat(),
            utils._get_name_project_most_recent() + '.pkl'
        )
    )

    messenger.message(['length_beats', str(length_beats)])

    stream_chord = utils_mxl.thaw_stream(
        os.path.join(
            utils.get_dirname_score(),
            'chord',
            utils._get_name_project_most_recent() + '.pkl'
        )
    )

    stream_upper_voices = postp_mxl.extract_upper_voices_stream(
        stream_chord
    )

    notes_live = convert_mxl.to_notes_live(
        stream_upper_voices
    )

    exporter = io_exporter.Exporter()

    exporter.set_part(notes_live, 'chord')

    exporter.export(utils.get_file_json_comm())

    messenger.message(['done', 'bang'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract Segments')

    args = parser.parse_args()

    main(args)
