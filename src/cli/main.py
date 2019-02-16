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
from information_retrieval import extraction as ir
from postprocess import midi as mid_post
import music21
from convert import musicxml as mxl
from filter import midi as filter_mid
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

    df = mesh_song.melody_to_df(
        data_melody,
        index_type='s'
    )

    # TODO: render using diff method
    df['melody'] = df['melody'].apply(handle_na).diff(1).cumsum().apply(librosa.hz_to_midi).round().apply(handle_na)

    # diff = hz_prep.remove_redundancies(
    #     data_melody[1]
    # )

    mesh_song.set_melody_tree(
        df
    )

    df_quantized = mesh_song._quantize(
        [beat['timestamp'] for beat in data_beats],
        s_beat_start,
        s_beat_end
    )

    score = mxl.df_grans_to_score(
        df_quantized
    )

    score.show()

    exit(0)

    non_empty_chords = vamp_filter.vamp_filter_non_chords(
        s_to_label_chords
    )

    events_chords = vamp_convert.vamp_to_dict(
        non_empty_chords
    )

    df_chords_quantized = song.MeshSong.quantize(
        song.MeshSong.chords_to_df(events_chords),
        [beat['timestamp'] for beat in data_beats],  # TODO: fix
        s_beat_start=s_beat_start,
        s_beat_end=s_beat_end
    )

    quantized_and_smoothed = filter_mid.smooth_chords(
        df_chords_quantized
    )

    score_quantized = mxl.df_beats_to_score(
        quantized_and_smoothed
    )

    # exit(0)
    # list_melody = data_melody[1]
    #
    # sample_rate = data_melody[0]
    #
    # df_melody_hz = pd.DataFrame(
    #     data={'melody': list_melody},
    #     index=[i_sample * sample_rate for i_sample, sample in enumerate(list_melody)]
    # )
    #
    # df_melody_hz.index.name = 's'
    #
    # chord = music21.harmony.ChordSymbol(s_to_label_chords[1]['label'].replace('b', '-'))

    df_upper_voicings = mid_post.extract_upper_voices(df_chords_quantized)

    mesh_song.add_chords(df_upper_voicings)

    # exit(0)

    # mesh_song.add_quantization(beatmap)

    # TODO: in actual workflow, shouldn't need to convert, as this will be taken care of in Ableton user assisted processing
    mesh_song.add_melody(
        midi_convert.hz_to_mid(
            mesh_song.melody_to_df(
                data_melody,
                index_type='s'
            )
        ),
        index_type='s'
    )

    mesh_song.add_pk()

    mesh_song.set_melody_tree(
    )

    exit(0)

    mesh_song.quantize_on_index(
        index='beat'
    )

    # TODO: segments, chords, and bass will have to be filled legato
    # TODO: ORRRR, this logic could be in "render"
    # mesh_song.fill_legato(name_column='chord')

    df_bass = mid_post.extract_bass(df_chords_quantized)

    mesh_song.add_bass(df_bass)

    df_segments = song.MeshSong.segments_to_df(data_segments)

    mesh_song.add_segments(
        df_segments
    )

    # file_chords_and_bass = ''
    stream_chords_and_bass = midi_convert.df_to_stream(
        columns=['chord', 'bass']
    )

    key_centers = analysis_midi.get_key_center_estimates(file_chords_and_bass)

    mesh_song.add_key_centers(key_centers)

    fixed_tempo_estimate = mir.get_fixed_tempo_estimate(tempomap)

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


