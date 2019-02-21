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

    # length of Ableton live track in beats

    beats_length_track_live = args.beats_length_track_live

    # beat start

    beat_start = args.beat_start

    # beat end

    beat_end = args.beat_end

    # length of wav file in s
    y, sr = librosa.load(utils.FILE_WAV)

    duration_s_audio = librosa.get_duration(y=y, sr=sr)

    s_beat_start = (beat_start / beats_length_track_live) * duration_s_audio

    s_beat_end = (beat_end / beats_length_track_live) * duration_s_audio

    df_melody = conv_max.to_df(
        filepath=utils.FILE_MELODY_FINAL
    )

    data_melody = ir.extract_melody(
        utils.FILE_WAV,
        from_cache=True
    )

    df_melody_diff = filt_mid.to_diff(
        conv_max.to_mid(
            df_melody,
            'melody'
        ),
        'melody',
        data_melody[0]
    )

    tree_melody = song.MeshSong.get_interval_tree(
        df_melody_diff
    )

    mesh_song = song.MeshSong()

    data_beats = ir.extract_beats(
        utils.FILE_WAV,
        from_cache=True
    )

    beatmap = prep_vamp.extract_beatmap(
        data_beats
    )

    mesh_song.set_tree(
        tree_melody,
        type='melody'
    )

    mesh_song.quantize(
        beatmap,
        s_beat_start,
        s_beat_end,
        columns=['melody']
    )

    df_data_quantized_diff = filt_mid.to_diff(
        mesh_song.data_quantized,
        name_column='melody',
        sample_rate=1/48  # (8, 6) quantization
    )

    score_melody = postp_mxl.df_grans_quantized_to_score(
        df_data_quantized_diff,
        parts=['melody']
    )

    dict_write_json_live = postp_mxl.to_json_live(
        score_melody,
        parts=['chord']
    )

    utils.to_json_live(
        dict_write_json_live,
        filename_chords_to_live=utils.FILE_MELODY_LIVE
    )

    postp_mxl.freeze_stream(
        stream=score_melody,
        filepath=utils.FILE_MELODY_SCORE
    )

    messenger.message(['done'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Quantize fully-processed melody and render to Live')

    parser.add_argument('beats_length_track_live', help='length of track in Live')

    parser.add_argument('beat_start', help='first beat in Live')

    parser.add_argument('beat_end', help='last beat in Live')

    args = parser.parse_args()

    main(args)
