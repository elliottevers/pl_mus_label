import sys
sys.path.insert(0, '/Users/elliottevers/Documents/git-repos.nosync/tk_music_py/src')
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

    stream_chord = utils_mxl.thaw_stream(
        os.path.join(
            utils.get_dirname_score(),
            'chord',
            utils._get_name_project_most_recent() + '.pkl'
        )
    )

    stream_upper_voices = postp_mxl.extract_upper_voices(
        stream_chord
    )

    notes_live = convert_mxl.to_notes_live(
        stream_upper_voices,
        beatmap,
        s_beat_start,
        s_beat_end,
        tempo
    )

    exporter = io_exporter.Exporter()

    exporter.set_part(notes_live, 'chord')

    exporter.export(utils.get_file_json_comm())

    messenger.message(['done', 'bang'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract Segments')

    args = parser.parse_args()

    main(args)
