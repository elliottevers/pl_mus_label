import vamp
import librosa
from mido import MidiFile, MidiTrack, Message, MetaMessage, bpm2tempo
from typing import List, Dict, Any, Optional, Tuple
import music21
import numpy as np

# data, rate = librosa.load(
#     "/Users/elliottevers/Documents/DocumentsSymlinked/git-repos.nosync/audio/youtube/tswift_teardrops.wav"
# )
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

# ms_to_label_chord: List[Dict[float, Any]] = vamp.collect(data, rate, 'nnls-chroma:chordino')['list']

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

# chord = music21.harmony.ChordSymbol(ms_to_label_chord[1]['label'].replace('b', '-'))
# chord.pitches  # ...

# for ms timeseries, treat bar estimates as framework to quantize segments and chords to
# TODO: symbolic segmentation - music21.search.segment.indexScoreParts?
testing = 1



mid = MidiFile('/Users/elliottevers/Documents/DocumentsSymlinked/git-repos.nosync/audio/ChordTracks/chords_tswift_tears.mid')

exit(0)

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

from abc import ABC, abstractmethod


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



# Note = Dict[]

events_chords: Dict[int, List[MidiNote]]

time_ms_last = 0


def ms_to_ticks(ms, bpm=60, ppq=480):

    quarter_notes_per_minute = bpm

    ticks_per_quarter_note = ppq

    ms_per_minute = (60 * 1000)

    ticks_per_minute = ticks_per_quarter_note * quarter_notes_per_minute

    ticks_per_ms = ticks_per_minute / ms_per_minute

    return ticks_per_ms * ms


for time_ms in list(events_chords.keys()):

    diff_ticks_last_event = ms_to_ticks(time_ms) - ms_to_ticks(time_ms_last)
    # for i_note, note in enumerate(events_chords[time_ms]):
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

    for i_note, note in enumerate(events_chords[time_ms_last]):
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
                    'note_on',
                    note=note.pitch,
                    velocity=note.velocity,
                    time=0
                )
            )

    for i_note, note in enumerate(events_chords[time_ms]):
        track.append(
            Message(
                'note_on',
                note=note.pitch,
                velocity=note.velocity,
                time=0
            )
        )

    time_ms_last = time_ms
