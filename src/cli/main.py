import vamp
import librosa
from mido import MidiFile, MidiTrack, Message, MetaMessage, bpm2tempo
from typing import List, Dict, Any, Optional, Tuple
import music21
import numpy as np
import pandas as pd
from music import note, song
from convert import midi as midi_convert, vamp as vamp_convert
from filter import vamp as vamp_filter
import jsonpickle
from analysis_discrete import music_xml as analysis_mxl
from information_retrieval import extraction as ir
from postprocess import midi as postp_mid, music_xml as postp_mxl, hz as hz_postp
import music21
from convert import musicxml as mxl_conv
from filter import midi as filter_mid, seconds as s_filt
from preprocess import hz as hz_prep, vamp as prep_vamp, seconds as s_prep
import math

# TODO: endow all structures with music21 instrument

filename_wav = "/Users/elliottevers/Documents/DocumentsSymlinked/git-repos.nosync/audio/youtube/tswift_teardrops.wav"

filename_mid_out = '/Users/elliottevers/Documents/DocumentsSymlinked/git-repos.nosync/audio/ChordTracks/chords_tswift_tears_TEST.mid'

branch = 'vamp'

s_beat_start = 3.436

s_beat_end = 26.9 + 3 * 60

data_melody = ir.extract_melody(
    filename_wav,
    stub=True
)

data_segments = ir.extract_segments(
    filename_wav,
    stub=True
)

data_chords = ir.extract_chords(
    filename_wav,
    stub=True
)

s_to_label_chords: List[Dict[float, Any]] = data_chords

data_tempo = ir.extract_tempo(
    filename_wav,
    stub=True
)

data_beats = ir.extract_beats(
    filename_wav,
    stub=True
)

# vamp branch of pipeline

mesh_song = song.MeshSong()


# def handle_na(h):
#     return 0 if not h or math.isinf(h) or math.isnan(h) or h < 0 else int(h)


# def to_midi(hz):
#     df_hz['melody'].apply(librosa.hz_to_midi).round()


if branch == 'vamp':

    # MELODY

    df_melody = prep_vamp.melody_to_df(
        data_melody,
        index_type='s'
    )

    # hertz pre-filtering -> discretization -> midi post-filtering -> postprocessing diff series (midi)
    df_melody['melody'] = hz_postp.get_diff(
        df_melody['melody']
    )

    tree_melody = song.MeshSong.get_interval_tree(
        df_melody
    )

    mesh_song.set_tree(
        tree_melody,
        type='melody'
    )

    # CHORDS

    # TODO: put in preprocessing module
    non_empty_chords = vamp_filter.vamp_filter_non_chords(
        s_to_label_chords
    )

    # TODO: put in preprocessing module
    events_chords: Dict[float, music21.chord.Chord] = vamp_convert.vamp_chord_to_dict(
        non_empty_chords
    )

    df_chords = prep_vamp.chords_to_df(
        events_chords
    )

    df_upper_voicings = postp_mxl.extract_upper_voices(
        df_chords
    )

    chord_tree = song.MeshSong.get_interval_tree(
        df_upper_voicings
    )

    mesh_song.set_tree(
        chord_tree,
        type='chord'
    )

    # BASS

    df_bass = postp_mxl.extract_bass(
        df_chords
    )

    tree_bass = song.MeshSong.get_interval_tree(
        df_bass
    )

    mesh_song.set_tree(
        tree_bass,
        type='bass'
    )

    # SEGMENTS

    df_segments = prep_vamp.segments_to_df(
        data_segments
    )

    tree_segments = song.MeshSong.get_interval_tree(
        df_segments
    )

    mesh_song.set_tree(
        tree_segments,
        type='segment'
    )

    # QUANTIZATION

    # TODO: using the interval trees, this adds the actual data
    # there should not be a multiindex df underneath the hood
    mesh_song.quantize(
        [beat['timestamp'] for beat in data_beats],
        s_beat_start,
        s_beat_end,
        columns=['melody', 'bass', 'chord', 'segment']
    )

    exit(0)

    # TODO: say something about using the "center of mass" of these structures to fix uncertainty at boundaries
    mesh_song.data_quantized['chord'] = filter_mid.smooth_chords(
        mesh_song.data_quantized['chord']
    )

    mesh_song.data_quantized['bass'] = filter_mid.smooth_bass(
        mesh_song.data_quantized['bass']
    )

    mesh_song.data_quantized['segments'] = filter_mid.smooth_segments(
        mesh_song.data_quantized['segments']
    )

    score_sans_key_centers = analysis_mxl.df_grans_to_score(
        mesh_song.data_quantized
    )

    # TODO: filter segments in the same way as chords, except using every *4* measures

    # KEY CENTERS

    stream_chords_and_bass = postp_mxl.extract_parts(
        score_sans_key_centers,
        parts=['chord', 'bass']
    )

    # TODO: give this dataframe an index of beats
    df_key_centers: pd.DataFrame = analysis_mxl.get_key_center_estimates(
        stream_chords_and_bass
    )

    mesh_song.add_key_centers(
        df_key_centers
    )

    # FIXED TEMPO ESTIMATE, FOR FINAL RENDERING

    tempomap = s_prep.tempo_to_df(
        data_tempo
    )

    # TODO: implement that median filter
    fixed_tempo_estimate = s_filt.get_fixed_tempo_estimate(
        tempomap
    )

    stream_score = mesh_song.to_score(

    )

    stream_score = postp_mxl.set_tempo(
        stream_score,
        fixed_tempo_estimate
    )

else:

    # web-based deep learning branch of pipeline

    # # TODO: extract relevant information to merge with other midi file
    # stream_chords: music21.stream.Stream, bpm_chords = prep_mid.load_stream(
    #     filename=''
    # )
    #
    # # TODO: put through series of transformations that will be performed manually in reality
    # stream_melody: music21.stream.Stream, bpm_melody = prep_mid.load_stream(
    #     filename=''
    # )

    # SEGMENTS

    # TODO: this might work better using chords
    stream_segments: music21.stream.Stream = analysis_mxl.get_segments(
        stream_melody
    )

    # KEY CENTERS
    stream_chords_and_bass: music21.stream.Stream = postp_mxl.extract_parts(
        stream_chords,
        parts=['chord', 'bass']
    )

    # TODO: give this dataframe an index of beats
    stream_key_centers: music21.stream.Stream = analysis_mxl.get_key_center_estimates(
        stream_chords_and_bass
    )

    stream_score = postp_mxl.combine_streams(
        stream_melody,
        stream_chords_and_bass,
        stream_segments,
        stream_key_centers
    )

    stream_score = postp_mxl.set_tempo(
        stream_score,
        bpm_chords
    )


song.MeshSong.render(
    stream_score
)

# TODO: notify Ableton Live that midi file is rendered

# TODO: use parser and encoder to bring parts to and from Ableton Live tracks



