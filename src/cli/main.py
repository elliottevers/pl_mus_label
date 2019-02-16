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
from analysis_discrete import midi as analysis_midi
from information_retrieval import extraction as mir
from postprocess import midi as postp_mid
import music21
from convert import musicxml as mxl_conv
from filter import midi as filter_mid, seconds as s_filt
from preprocess import hz as hz_prep
import math


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


def handle_na(h):
    return 0 if not h or math.isinf(h) or math.isnan(h) or h < 0 else int(h)


# def to_midi(hz):
#     df_hz['melody'].apply(librosa.hz_to_midi).round()


if branch == 'vamp':

    # MELODY

    df_melody = prep_vamp.melody_to_df(
        data_melody,
        index_type='s'
    )

    # map hertz to midi
    # TODO: put in preprocessing module
    df_melody['melody'] = df_melody['melody'].apply(handle_na).diff(1).cumsum().apply(librosa.hz_to_midi).round().apply(handle_na)

    mesh_song.set_melody_tree(
        df_melody
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

    df_upper_voicings = postp_mid.extract_upper_voices(
        df_chords
    )

    mesh_song.set_chord_tree(
        df_upper_voicings
    )

    # BASS

    df_bass = postp_mid.extract_bass(
        df_chords
    )

    mesh_song.set_bass_tree(
        df_bass
    )

    # SEGMENTS

    df_segments = prep_vamp.segments_to_df(
        data_segments
    )

    mesh_song.set_segment_tree(
        df_segments
    )

    # QUANTIZATION

    # TODO: using the interval trees, this adds the actual data
    # there should not be a multiindex df underneath the hood
    mesh_song.quantize(
        [beat['timestamp'] for beat in data_beats],
        s_beat_start,
        s_beat_end,
        columns=['melody', 'bass', 'chords', 'segments']
    )

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

    score_sans_key_centers = mxl.df_grans_to_score(
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

else:

    # web-based deep learning branch of pipeline

    # NB: already quantized
    chords = postprocess.load_df(
        filename=''  # chordify download location
    )

    # NB: no conversion from hertz to midi necessary
    melody = postprocess.load_df(
        filename=''  # Ableton transcription download location
    )

    bass = postprocess.extract_bass(chords)

    upper_voicings = postprocess.extract_upper_voicings(chords)

    mesh_song.add_chords(upper_voicings)

    mesh_song.add_bass(bass)

    mesh_song.add_melody(
        melody=melody
    )

    segments = analysis_midi.extract_segments()

    file_chords_and_bass = ''

    key_centers = analysis_midi.get_key_center_estimates(file_chords_and_bass)

    mesh_song.add_key_centers(key_centers)

    fixed_tempo_estimate = postprocessing.extract_bpm(filename_mid='')


mesh_song.render(
    part_to_track=part_track_map,
    type='fixed_tempo',
    tempo=fixed_tempo_estimate
)


