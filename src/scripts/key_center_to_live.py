from information_retrieval import extraction as ir
from filter import seconds as s_filt
from preprocess import vamp as prep_vamp
from message import messenger as mes
from filter import hertz as filt_hz, midi as filt_mid
from utils import utils
from convert import max as conv_max
import argparse
from music import song
from typing import Dict
import librosa
from postprocess import music_xml as postp_mxl


def filter(params, type_substrate):
    if type_substrate == 'hz':
        df_filtered = filt_hz.apply_filters(
            params
        )
    elif type_substrate == 'mid':
        df_filtered = filt_mid.apply_filters(
            params
        )
    else:
        raise 'substrate type ' + type_substrate + ' not supported'

    return df_filtered


def main(args):
    messenger = mes.Messenger()

    messenger.message(['running'])

    index_key_center_filtered_chosen = args.index_melody_mid_filtered_chosen

    # data_beats = ir.extract_beats(
    #     utils.FILE_WAV,
    #     from_cache=True
    # )
    #
    # beatmap = prep_vamp.extract_beatmap(
    #     data_beats
    # )

    df_key_center_filtered_chosen = conv_max.from_coll(
        filepath=utils.get_path_key_center_filtered(
            index_key_center_filtered_chosen
        )
    )

    dict_write_json_live = postp_mxl.to_json_live(
        score_key_center,
        parts=['key_center']
    )

    utils.to_json_live(
        dict_write_json_live,
        filename_chords_to_live=utils.FILE_KEY_CENTER_LIVE
    )
    #
    # postp_mxl.freeze_stream(
    #     stream=score_melody,
    #     filepath=utils.FILE_MELODY_SCORE
    # )

    messenger.message(['done'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Quantize fully-processed melody and render to Live')

    parser.add_argument('beats_length_track_live', help='length of track in Live')

    parser.add_argument('beat_start', help='first beat in Live')

    parser.add_argument('beat_end', help='last beat in Live')

    args = parser.parse_args()

    main(args)
