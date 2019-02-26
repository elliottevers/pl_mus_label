from information_retrieval import extraction as ir
from message import messenger as mes
import argparse
import librosa
from typing import List, Dict, Any
from filter import vamp as vamp_filter
from convert import vamp as vamp_convert
from preprocess import vamp as prep_vamp
from postprocess import music_xml as postp_mxl, midi as postp_mid
from music import song
import music21
import json
from utils import utils
from convert import max as conv_max
from analysis_discrete import music_xml as analysis_mxl


# TODO: get the filepath of the cache module
filename_chords_to_live = utils.get_path_cache(utils.CHORD_LIVE)


def main(args):
    messenger = mes.Messenger()

    messenger.message(['running'])

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

    # filename_wav = args.filename

    score_chords = postp_mxl.thaw_stream(
        utils.FILE_CHORD_SCORE
    )

    # SCORE UPPER VOICES

    # TODO: postp_mxl should be agnostic to dataframes
    score_upper_voicings = postp_mxl.extract_upper_voices(
        score_chords
    )

    # SCORE BASS

    score_bass = postp_mxl.extract_bass(
        score_chords
    )

    score_upper_voicings_and_bass = postp_mxl.combine_streams(
        score_upper_voicings,
        score_bass,
    )

    part_key_centers: music21.stream.Part = analysis_mxl.get_key_center_estimates(
        score_upper_voicings_and_bass
    )

    # score to quantized df

    df_key_center_quantized = postp_mxl.part_to_df_quantized(
        part_key_centers
    )

    # TODO: need to render alongside of audio file in Ableton Live track, so need beatmap

    data_beats = ir.extract_beats(
        utils.FILE_WAV,
        from_cache=True
    )

    beatmap = prep_vamp.extract_beatmap(
        data_beats
    )

    df_key_center_synced = postp_mid.add_index_s(
        df_key_center_quantized,
        beatmap,
        s_beat_start,
        s_beat_end
    )

    df_synced_and_embellished = filt_mid.interpolate(
        df_key_center_synced,
        sample_rate=.0029
    )

    conv_max.to_coll(
        df_synced_and_embellished,
        filepath=utils.FILE_COLL_KEY_CENTER_RAW
    )

    messenger.message(
        [
            utils.MESSAGE_FILE_COLL,
            utils.FILE_COLL_KEY_CENTER_RAW
        ]
    )

    # score_full = postp_mxl.combine_streams(
    #     score_melody,
    #     score_bass,
    #     score_chord,
    #     score_segment,
    #     score_key_center
    # )
    #
    # postp_mxl.thaw_stream(
    #     score_full,
    #     utils.FILE_SCORE_FULL
    # )

    messenger.message(['done'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract Melody')

    # parser.add_argument('beats_length_track_live', help='length of track in Live')
    #
    # parser.add_argument('beat_start', help='first beat in Live')
    #
    # parser.add_argument('beat_end', help='last beat in Live')

    args = parser.parse_args()

    main(args)
