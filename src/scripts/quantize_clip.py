from message import messenger as mes
import argparse
from utils import utils
from i_o import importer as io_importer, exporter as io_exporter
from convert import music_xml as convert_mxl


def main(args):

    name_part = args.name_part.replace("\"", '')

    beat_multiple_quantization = args.beat_multiple.replace("\"", '')

    quarter_length_divisor = 1/float(beat_multiple_quantization)

    importer = io_importer.Importer(
        utils.get_file_json_comm()
    )

    importer.load([name_part])

    notes_live = importer.get_part(name_part)

    # convert ableton live notes to stream

    from postprocess import music_xml as postp_mxl

    mode = 'polyphonic' if name_part == 'chord' else 'monophonic'

    stream = postp_mxl.live_to_stream(
        notes_live,
        mode
    )

    stream.quantize(
        (quarter_length_divisor, ),
        inPlace=True
    )

    notes_live = convert_mxl.to_notes_live(
        stream
    )

    exporter = io_exporter.Exporter()

    exporter.set_part(notes_live, name_part)

    exporter.export(utils.get_file_json_comm())

    messenger = mes.Messenger()

    messenger.message(['done'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Quantize Chords')

    parser.add_argument('--beat_multiple', help='e.g., if 4, quantize to the measure')

    parser.add_argument('--name_part', help='e.g., if 4, quantize to the measure')

    args = parser.parse_args()

    main(args)
