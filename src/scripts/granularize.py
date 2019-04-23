from message import messenger as mes
import argparse
from utils import utils
from i_o import importer as io_importer, exporter as io_exporter
from convert import music_xml as convert_mxl


def main(args):

    name_part = utils.parse_arg(args.name_part)

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

    stream = convert_mxl.live_to_stream(
        notes_live,
        beatmap=beatmap,
        s_beat_start=s_beat_start,
        s_beat_end=s_beat_end,
        tempo=tempo,
        mode=mode
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
