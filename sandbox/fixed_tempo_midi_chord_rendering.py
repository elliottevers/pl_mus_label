import vamp
import librosa
from mido import MidiFile, MidiTrack, Message, MetaMessage, bpm2tempo
from typing import List, Dict, Any, Optional, Tuple
import music21
import numpy as np
import pandas as pd
from music import note
from convert import midi as midi_convert

# from abc import ABC, abstractmethod

filename_wav = "/Users/elliottevers/Documents/DocumentsSymlinked/git-repos.nosync/audio/youtube/tswift_teardrops.wav"

filename_mid_out = '/Users/elliottevers/Documents/DocumentsSymlinked/git-repos.nosync/audio/ChordTracks/chords_tswift_tears_TEST.mid'

data, rate = librosa.load(
    filename_wav
)
#
# # TODO: melody extraction
# melody = vamp.collect(data, rate, "mtg-melodia:melodia")
#
# type(melody['vector'][1])
#
# testing = 1

# TODO: segments - quantize to nearest two bar multiple
# import vamp
# import librosa
# segments = vamp.collect(data, rate, 'qm-vamp-plugins:qm-segmenter')

# test = 1

# TODO: chords
# ms_to_label_chord: List[Dict[float, Any]] = vamp.collect(data, rate, 'nnls-chroma:chordino')['list']

s_to_label_chords: List[Dict[float, Any]] = vamp.collect(data, rate, 'nnls-chroma:chordino')['list']

# testing = 1

# TODO: rolling tempo estimate

# tempo: List[Dict[float, Any]] = vamp.collect(data, rate, 'vamp-aubio:aubiotempo', 'tempo')['vector'][1]
# bpm = np.median(tempo)  # smoothing
# testing = 1

# TODO: measures

beats: List[Dict[float, Any]] = vamp.collect(data, rate, 'qm-vamp-plugins:qm-barbeattracker')['list']
#
# testing = 1

# TODO: music21 chord parsing

chord = music21.harmony.ChordSymbol(s_to_label_chords[1]['label'].replace('b', '-'))
# chord.pitches  # ...

# for ms timeseries, treat bar estimates as framework to quantize segments and chords to
# TODO: symbolic segmentation - music21.search.segment.indexScoreParts?
# testing = 1

mid = MidiFile(
    ticks_per_beat=1000
)

events_chords: Dict[float, List[note.MidiNote]] = dict()


def quantize_numeric_domain(events_chords: Dict[float, List[note.MidiNote]], beats: List[float]) -> Dict[float, List[note.MidiNote]]:

    events_quantized: Dict[float, List[note.MidiNote]] = dict()

    for s, chord in events_chords.items():
        key_s_quantized = min(list(beats), key=lambda s_beat: abs(s_beat - s))
        events_quantized[key_s_quantized] = chord

    return events_quantized


# non empty
chords = list(filter(lambda event_chord: event_chord['label'] != 'N', s_to_label_chords))

for chord in chords:
    duration_ticks = None  # TODO: calculate here, instead of during midi file creation
    velocity = 90
    chord_realized = music21.harmony.ChordSymbol(chord['label'].replace('b', '-'))
    events_chords[chord['timestamp'].to_float()] = [
        note.MidiNote(pitch.midi, duration_ticks, velocity) for pitch in chord_realized.pitches
    ]

# quantized
chords = quantize_numeric_domain(events_chords, [beat['timestamp'].to_float() for beat in beats])


class Garbage(object):
    def __init__(self, data):
        self.data = data


first_event = {
    1: 'A',
    2: 'C#',
    3: 'E'
}

second_event = {
    1: 'C',
    2: 'E',
    3: 'G'
}


from music import song

# song = song.MeshSong()

# TODO: determine first and last beat in seconds, then debug

s_beat_start = 3.436

s_beat_end = 26.9 + 3 * 60

df_chords_quantized = song.MeshSong.quantize(
    song.MeshSong.to_df(events_chords),
    [beat['timestamp'].to_float() for beat in beats],
    s_beat_start=s_beat_start,
    s_beat_end=s_beat_end
)

track = midi_convert.df_to_mid(df_chords_quantized, label_part='chord')

exit(0)


def extract_bpm(filename: str):
    data, rate = librosa.load(
       filename
    )

    tempo: List[Dict[float, Any]] = vamp.collect(data, rate, 'vamp-aubio:aubiotempo', 'tempo')['vector'][1]

    return np.median(tempo)  # smoothing


# bpm = extract_bpm(
#     "/Users/elliottevers/Documents/DocumentsSymlinked/git-repos.nosync/audio/youtube/tswift_teardrops.wav"
# )

