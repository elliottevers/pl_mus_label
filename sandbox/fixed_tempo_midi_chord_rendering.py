import vamp
import librosa
from mido import MidiFile, MidiTrack, Message, MetaMessage, bpm2tempo
from typing import List, Dict, Any, Optional, Tuple
import music21
import numpy as np
import pandas as pd
from music import note
from convert import midi as midi_convert, vamp as vamp_convert
from filter import vamp as vamp_filter
import jsonpickle

filename_wav = "/Users/elliottevers/Documents/DocumentsSymlinked/git-repos.nosync/audio/youtube/tswift_teardrops.wav"

filename_mid_out = '/Users/elliottevers/Documents/DocumentsSymlinked/git-repos.nosync/audio/ChordTracks/chords_tswift_tears_TEST.mid'

data, rate = librosa.load(
    filename_wav
)

# length_s = librosa.core.get_duration(
#     filename=filename_wav
# )

# length_s = 219.86975056689343

# TODO: melody extraction
# melody = vamp.collect(data, rate, "mtg-melodia:melodia")
#
# sample_rate = melody['vector'][0].to_float()
#
# melody_extracted = melody['vector'][1]
#
# data_melody = (sample_rate, melody_extracted)

# with open('test/stubs_pickle/python/melody_tswift_teardrops.json', 'w') as file:
#     file.write(jsonpickle.encode(data_melody))

# with open('test/stubs_pickle/python/melody_tswift_teardrops.json', 'w') as file:
#     file.write(jsonpickle.encode(melody))

# with open('test/stubs_pickle/python/melody_tswift_teardrops.json', 'r') as file:
#     melody = jsonpickle.decode(file.read())

with open('test/stubs_pickle/python/melody_tswift_teardrops.json', 'r') as file:
    data_melody = jsonpickle.decode(file.read())


# testing =1


# exit(0)
#
# type(melody['vector'][1])
#
# testing = 1

# TODO: segments - quantize to nearest two bar multiple
# import vamp
# import librosa
# segments = vamp.collect(data, rate, 'qm-vamp-plugins:qm-segmenter')
#
# data_segments = [
#     {
#         'timestamp': segment['timestamp'].to_float(),
#         'duration': segment['duration'].to_float(),
#         'label': segment['label'],
#         'values': segment['values']
#     }
#     for segment
#     in segments['list']
# ]
#
# with open('test/stubs_pickle/python/segments_tswift_teardrops.json', 'w') as file:
#     file.write(jsonpickle.encode(data_segments))


with open('test/stubs_pickle/python/segments_tswift_teardrops.json', 'r') as file:
    data_segments = jsonpickle.decode(file.read())

# test = 1

# exit(0)

# TODO: chords
# ms_to_label_chord: List[Dict[float, Any]] = vamp.collect(data, rate, 'nnls-chroma:chordino')['list']

# chords = vamp.collect(data, rate, 'nnls-chroma:chordino')
#
# data_chords = [
#     {
#         'timestamp': chord['timestamp'].to_float(),
#         'label': chord['label']
#     }
#     for chord
#     in chords['list']
# ]
#
# with open('test/stubs_pickle/python/chords_tswift_teardrops.json', 'w') as file:
#     file.write(jsonpickle.encode(data_chords))


with open('test/stubs_pickle/python/chords_tswift_teardrops.json', 'r') as file:
    data_chords = jsonpickle.decode(file.read())

s_to_label_chords: List[Dict[float, Any]] = data_chords  # chords['list']

# exit(0)
# TODO: rolling tempo estimate

# tempo = vamp.collect(data, rate, 'vamp-aubio:aubiotempo', 'tempo')
#
# sample_rate = tempo['vector'][0].to_float()
#
# tempo_estimates = tempo['vector'][1]
#
# data_tempo = (sample_rate, tempo_estimates)
#
# with open('test/stubs_pickle/python/tempo_tswift_teardrops.json', 'w') as file:
#     file.write(jsonpickle.encode(data_tempo))

with open('test/stubs_pickle/python/tempo_tswift_teardrops.json', 'r') as file:
    tempo_thawed = jsonpickle.decode(file.read())
#
# tempo: List[Dict[float, Any]] = tempo['vector'][1]
# exit(0)
# bpm = np.median(tempo)  # smoothing
# testing = 1


# TODO: measures

# beats = vamp.collect(data, rate, 'qm-vamp-plugins:qm-barbeattracker')
#
# data_beats = [
#     {
#         'timestamp': beat['timestamp'].to_float(),
#         'label': beat['label']
#     }
#     for beat
#     in beats['list']
# ]
#
#
# with open('test/stubs_pickle/python/beats_tswift_teardrops.json', 'w') as file:
#     file.write(jsonpickle.encode(data_beats))
#
#
with open('test/stubs_pickle/python/beats_tswift_teardrops.json', 'r') as file:
    beats_thawed = jsonpickle.decode(file.read())
#
# beats: List[Dict[float, Any]] = beats['list']
#
# exit(0)
#
# testing = 1

# TODO: music21 chord parsing

list_melody = data_melody[1]

sample_rate = data_melody[0]

df_melody_hz = pd.DataFrame(
    data=list_melody,
    index=[i_sample * sample_rate for i_sample, sample in enumerate(list_melody)]
)

chord = music21.harmony.ChordSymbol(s_to_label_chords[1]['label'].replace('b', '-'))

# chord.pitches  # ...

# for ms timeseries, treat bar estimates as framework to quantize segments and chords to
# TODO: symbolic segmentation - music21.search.segment.indexScoreParts?
# testing = 1

mid = MidiFile(
    ticks_per_beat=1000
)


# TODO: fix
non_empty_chords = vamp_filter.vamp_filter_non_chords(
    chords
)

events_chords = vamp_convert.vamp_to_dict(
    non_empty_chords
)


# exit(0)


def quantize_numeric_domain(events_chords: Dict[float, List[note.MidiNote]], beats: List[float]) -> Dict[float, List[note.MidiNote]]:

    events_quantized: Dict[float, List[note.MidiNote]] = dict()

    for s, chord in events_chords.items():
        key_s_quantized = min(list(beats), key=lambda s_beat: abs(s_beat - s))
        events_quantized[key_s_quantized] = chord

    return events_quantized


# non empty
# chords = list(filter(lambda event_chord: event_chord['label'] != 'N', s_to_label_chords))
#
# for chord in chords:
#     duration_ticks = None  # TODO: calculate here, instead of during midi file creation
#     velocity = 90
#     chord_realized = music21.harmony.ChordSymbol(chord['label'].replace('b', '-'))
#     events_chords[chord['timestamp'].to_float()] = [
#         note.MidiNote(pitch.midi, duration_ticks, velocity) for pitch in chord_realized.pitches
#     ]

# quantized
# chords = quantize_numeric_domain(events_chords, [beat['timestamp'].to_float() for beat in beats])


# class Garbage(object):
#     def __init__(self, data):
#         self.data = data
#
#
# first_event = {
#     1: 'A',
#     2: 'C#',
#     3: 'E'
# }
#
# second_event = {
#     1: 'C',
#     2: 'E',
#     3: 'G'
# }


from music import song

# song = song.MeshSong()

# TODO: determine first and last beat in seconds, then debug

s_beat_start = 3.436

s_beat_end = 26.9 + 3 * 60

df_chords_quantized = song.MeshSong.quantize(
    song.MeshSong.to_df(events_chords),
    [beat['timestamp'].to_float() for beat in beats], # TODO: fix
    s_beat_start=s_beat_start,
    s_beat_end=s_beat_end
)

track = midi_convert.df_to_mid(df_chords_quantized, label_part='chord')

# exit(0)


def extract_bpm(filename: str):
    data, rate = librosa.load(
       filename
    )

    tempo: List[Dict[float, Any]] = vamp.collect(data, rate, 'vamp-aubio:aubiotempo', 'tempo')['vector'][1]

    return np.median(tempo)  # smoothing


# bpm = extract_bpm(
#     "/Users/elliottevers/Documents/DocumentsSymlinked/git-repos.nosync/audio/youtube/tswift_teardrops.wav"
# )

