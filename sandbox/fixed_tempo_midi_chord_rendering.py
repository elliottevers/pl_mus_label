import vamp
import librosa
from mido import MidiFile, MidiTrack, Message, MetaMessage, bpm2tempo
from typing import List, Dict, Any, Optional, Tuple
import music21
import numpy as np
import pandas as pd

from abc import ABC, abstractmethod

filename_wav = "/Users/elliottevers/Documents/DocumentsSymlinked/git-repos.nosync/audio/youtube/tswift_teardrops.wav"

filename_mid_out = '/Users/elliottevers/Documents/DocumentsSymlinked/git-repos.nosync/audio/ChordTracks/chords_tswift_tears_TEST.mid'


class Note(ABC):

    def __init__(self, pitch, duration):
        super().__init__()
        self.pitch = pitch
        self.duration = duration

    # @abstractmethod
    # def do_something(self):
    #     pass


class MidiNote(Note):

    pitch: int

    duration: int

    velocity: int

    def __init__(self, pitch, duration_ticks, velocity):
        super().__init__(pitch, duration_ticks)
        self.pitch = pitch
        self.duration = duration_ticks
        self.velocity = velocity

data, rate = librosa.load(
    "/Users/elliottevers/Documents/DocumentsSymlinked/git-repos.nosync/audio/youtube/tswift_teardrops.wav"
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

# beats: List[Dict[float, Any]] = vamp.collect(data, rate, 'qm-vamp-plugins:qm-barbeattracker')['list']
#
# testing = 1

# TODO: music21 chord parsing

chord = music21.harmony.ChordSymbol(s_to_label_chords[1]['label'].replace('b', '-'))
# chord.pitches  # ...

# for ms timeseries, treat bar estimates as framework to quantize segments and chords to
# TODO: symbolic segmentation - music21.search.segment.indexScoreParts?
# testing = 1



mid = MidiFile(
    # '/Users/elliottevers/Documents/DocumentsSymlinked/git-repos.nosync/audio/ChordTracks/chords_tswift_tears.mid'
)

events_chords: Dict[float, List[MidiNote]] = dict()

# number_list = range(-5, 5)
# less_than_zero = list(filter(lambda x: x < 0, number_list))
# print(less_than_zero)

# def to_float(self):  # real signature unknown; restored from __doc__
#     """ to_float() -> Floating point representation. """
#     pass
#
#
# def to_frame(self, samplerate):  # real signature unknown; restored from __doc__
#     """ to_frame(samplerate) -> Sample count for given sample rate. """
#     pass
#
#
# def to_string(self):  # real signature unknown; restored from __doc__
#     """ to_string() -> Return a user-readable string to the nearest millisecond in a form like HH:MM:SS.mmm """
#     pass
#
#
# def values(self):  # real signature unknown; restored from __doc__
#     """ values() -> Tuple of sec,nsec representation. """
#     pass


non_empty_chords = list(filter(lambda event_chord: event_chord['label'] != 'N', s_to_label_chords))

for chord in non_empty_chords:
    duration_ticks = None  # TODO: calculate here, instead of during midi file creation
    velocity = 90
    chord_realized = music21.harmony.ChordSymbol(chord['label'].replace('b', '-'))
    events_chords[chord['timestamp'].to_float()] = [
        MidiNote(pitch.midi, duration_ticks, velocity) for pitch in chord_realized.pitches
    ]


# exit(0)

track = MidiTrack()

mid.tracks.append(track)

track.append(
    Message(
        'program_change',
        program=22,
        time=0
    )
)

iter_tick = 0

tick_last = 0

ticks = []

notes_midi = []


def extract_bpm(filename: str):
    data, rate = librosa.load(
       filename
    )

    tempo: List[Dict[float, Any]] = vamp.collect(data, rate, 'vamp-aubio:aubiotempo', 'tempo')['vector'][1]

    return np.median(tempo)  # smoothing


# bpm = extract_bpm(
#     "/Users/elliottevers/Documents/DocumentsSymlinked/git-repos.nosync/audio/youtube/tswift_teardrops.wav"
# )

bpm = 100  # testing

ppq = 384

# quarter_notes_per_minute = bpm
#
# ticks_per_quarter_note = ppq
#
# ms_per_minute = (60 * 1000)
#
# ticks_per_minute = ticks_per_quarter_note * quarter_notes_per_minute
#
# ticks_per_ms = ticks_per_minute / ms_per_minute

track.append(
    MetaMessage(
        'time_signature',
        time=0
    )
)

track.append(
    MetaMessage(
        'set_tempo',
        tempo=bpm2tempo(bpm),
        time=0
    )
)


def ms_to_ticks(s, bpm=60, ppq=480):

    quarter_notes_per_minute = bpm

    ticks_per_quarter_note = ppq

    ms_per_minute = (60 * 1000)

    ticks_per_minute = ticks_per_quarter_note * quarter_notes_per_minute

    ticks_per_ms = ticks_per_minute / ms_per_minute

    ms_per_second = 1000

    return int(ticks_per_ms * ms_per_second * s)


time_s_last = list(events_chords.keys())[0]


for time_s in list(events_chords.keys())[1:]:

    diff_ticks_last_event = ms_to_ticks(time_s, bpm=bpm, ppq=ppq) - ms_to_ticks(time_s_last, bpm=bpm, ppq=ppq)
    # for i_note, note in enumerate(events_chords[time_s]):
    #     if i_note == 0:
    #         track.append(
    #             Message(
    #                 'note_on',
    #                 note=note.pitch,
    #                 velocity=note.velocity,
    #                 time=diff_ticks_last_event
    #             )
    #         )
    #     else:
    #         track.append(
    #             Message(
    #                 'note_on',
    #                 note=note.pitch,
    #                 velocity=note.velocity,
    #                 time=0
    #             )
    #         )

    for i_note, note in enumerate(events_chords[time_s_last]):
        if i_note == 0:
            track.append(
                Message(
                    'note_off',
                    note=note.pitch,
                    velocity=note.velocity,
                    time=diff_ticks_last_event
                )
            )
        else:
            track.append(
                Message(
                    'note_off',
                    note=note.pitch,
                    velocity=note.velocity,
                    time=0
                )
            )

    for i_note, note in enumerate(events_chords[time_s]):
        track.append(
            Message(
                'note_on',
                note=note.pitch,
                velocity=note.velocity,
                time=0
            )
        )

    time_s_last = time_s


mid.save(filename_mid_out)