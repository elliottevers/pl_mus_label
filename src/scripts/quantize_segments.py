from information_retrieval import extraction as ir
from message import messenger as mes
import argparse
from utils import utils
from postprocess import music_xml as postp_mxl


def main(args):
    messenger = mes.Messenger()

    messenger.message(['running'])

    beat_multiple_quantization = args.beat_multiple_quantization

    quarter_length_divisor = 1/beat_multiple_quantization

    stream_segments = postp_mxl.thaw_stream(
        utils.FILE_SEGMENT_SCORE
    )

    stream_segments.quantize(
        (quarter_length_divisor, ),
        inPlace=True
    )

    postp_mxl.freeze_stream(
        utils.FILE_SEGMENT_SCORE,
        utils.FILE_SEGMENT_SCORE
    )

    dict_write_json_live = postp_mxl.to_json_live(
        stream_segments,
        parts=['segment']
    )

    utils.to_json_live(
        dict_write_json_live,
        filename_segments_to_live=utils.FILE_SEGMENT_LIVE
    )

    messenger.message(['done'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Quantize Segments')

    parser.add_argument('beat_multiple_quantization', help='e.g., if 4, quantize to the measure')

    args = parser.parse_args()

    main(args)
