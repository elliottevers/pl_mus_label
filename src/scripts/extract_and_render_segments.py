from information_retrieval import extraction as ir
from message import messenger as mes
import argparse
import librosa
from typing import List, Dict, Any
from filter import vamp as vamp_filter
from convert import vamp as vamp_convert
from preprocess import vamp as prep_vamp
from postprocess import music_xml as postp_mxl
from music import song
import music21
import json
from utils import utils


# TODO: get the filepath of the cache module
filename_chords_to_live = utils.get_path_cache(utils.CHORD_LIVE)


def main(args):
    messenger = mes.Messenger()

    messenger.message(['running'])

    filename_wav = utils.FILE_WAV_DOWNLOADED

    # length of Ableton live track in beats
    # TODO: this is for ms -> beat mapping for rendering to Ableton Live alongside raw audio
    beats_length_track_live = args.beats_length_track_live

    # beat start

    beat_start = args.beat_start

    # beat end

    beat_end = args.beat_end

    # length of wav file in s
    y, sr = librosa.load(filename_wav)

    duration_s_audio = librosa.get_duration(y=y, sr=sr)

    s_beat_start = (beat_start / beats_length_track_live) * duration_s_audio

    s_beat_end = (beat_end / beats_length_track_live) * duration_s_audio

    data_segments = ir.extract_segments(
        utils.FILE_WAV_DOWNLOADED
    )

    df_segments = prep_vamp.segments_to_df(
        data_segments
    )

    tree_segments = song.MeshSong.get_interval_tree(
        df_segments
    )

    mesh_song = song.MeshSong()

    mesh_song.set_tree(
        tree_segments,
        type='segment'
    )

    data_beats = ir.extract_beats(
        utils.FILE_WAV_DOWNLOADED,
        from_cache=True
    )

    beatmap = prep_vamp.extract_beatmap(
        data_beats
    )

    mesh_song.set_tree(
        tree_segments,
        type='segment'
    )

    mesh_song.quantize(
        beatmap,
        s_beat_start,
        s_beat_end,
        columns=['segment']
    )

    # index beat, index ms audio file, index beat live audio track
    df_with_live_audio_index = song.MeshSong.add_live_index(
        mesh_song.data_quantized,
        beat_start_live=beat_start,
        beat_end_live=beat_end,
        beats_length_track_live=beats_length_track_live
    )

    # TODO: save Live JSON for chords synced with audio track in Live
    # NB: this should have an index of beats in Live
    dict_write_json_live = song.MeshSong.to_json_live(
        df_with_live_audio_index,
        columns=['segment']
    )

    utils.to_json_live(
        dict_write_json_live,
        filename_chords_to_live=utils.FILE_SEGMENT_TO_LIVE
    )

    score_segment = postp_mxl.df_grans_to_score(
        df_with_live_audio_index,
        parts=['segment']
    )

    postp_mxl.freeze_stream(
        stream=score_segment,
        filepath=utils.SCORE_SEGMENT
    )

    messenger.message(['done'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract Chords')

    parser.add_argument('beats_length_track_live', help='length of track in Live')

    parser.add_argument('beat_start', help='first beat in Live')

    parser.add_argument('beat_end', help='last beat in Live')

    args = parser.parse_args()

    main(args)
