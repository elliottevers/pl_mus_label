import pandas as pd
import music21
from typing import List, Dict, Any, Optional, Tuple
# from music import note as lib_note, song, chord as lib_chord
import music21
from live import note as note_live
import numpy as np
from postprocess import music_xml as postp_mxl


# def df_beats_to_score(df: pd.DataFrame, column_index='beat', partmap={'chord': 0}) -> music21.stream.Score:
#
#     beat_last = max(df.index.get_level_values(column_index))
#
#     parts = []
#
#     for name_part, position in partmap.items():
#         part = music21.stream.Part()
#         part.id = name_part
#         parts.append(part)
#
#     part = parts[0]
#
#     measure = music21.stream.Measure()
#
#     for beat in range(1, beat_last):
#         if beat % 4 == 1:
#             part.append(measure)
#             measure = music21.stream.Measure()
#         chord: lib_chord.ChordMidi = df.loc[(beat, slice(None)), 'chord'].values[0]
#         measure.append(
#             music21.chord.Chord(
#                 [music21.pitch.Pitch(midi=chord_midi.pitch).name for chord_midi in chord.notes],
#                 duration=music21.duration.Duration(1.0)
#             )
#         )
#
#     score = music21.stream.Score()
#
#     score.insert(0, part)
#
#     return score


# TODO: put in module
def struct_to_notes_live(struct_21, name_part):
    try:
        if struct_21.name == 'rest':
            return []
    except AttributeError:
        pass

    notes = []

    if name_part == 'melody':
        # if not object > 0:
        #     struct_score = note.Rest()
        # else:
        #     struct_score = note.Note(
        #         pitch=pitch.Pitch(
        #             midi=int(object)
        #         )
        #     )
        testing = 1
    elif name_part == 'chord':
        beats_offset = float(struct_21.offset)
        beats_duration = float(struct_21.duration.quarterLength)
        velocity = 90
        muted = 0

        for pitch in struct_21.pitches:
            notes.append(
                note_live.NoteLive.parse(
                    [pitch.midi, beats_offset, beats_duration, velocity, muted]
                )
            )

    elif name_part == 'bass':
        # struct_score = note.Note(
        #     pitch=object
        # )
        testing = 1
    elif name_part == 'segment':
        # struct_score = note.Note(
        #     pitch=pitch.Pitch(
        #         midi=60
        #     )
        # )
        testing = 1
    else:
        raise 'part ' + name_part + ' not able to be converted to Live'

    return notes


def notes_live_to_struct():
    return

# TODO: not generalized to chords yet

def from_notes_live(notes_live, name_part):  # -> music21.stream.Stream:

    part = music21.stream.Part()

    part.id = name_part

    for note in notes_live:
        dur = music21.duration.Duration(note.beats_duration)

        part.insert(
            note.beat_start,
            postp_mxl.get_struct_score(
                note.pitch,
                name_part,
                dur
            )
        )

    return part


def to_note_live(note_21):
    return note_live.NoteLive(
        pitch=int(note_21.pitch.midi),
        beat_start=float(note_21.offset),
        beats_duration=float(note_21.duration.quarterLength),
        velocity=90,
        muted=0
    )


# self.pitch = pitch
# self.beat_start = beat_start
# self.beats_duration = beats_duration
# self.velocity = velocity
# self.muted = muted


def to_notes_live(stream):
    notes_live = []
    for note_21 in stream:
        notes_live.append(to_note_live(note_21))
    return notes_live


# # TODO: abstract to any part
# def df_grans_to_score(df_grans: pd.DataFrame, column_index='beat', partmap={'melody': 0}) -> music21.stream.Score:
#     parts = []
#
#     for name_part, position in partmap.items():
#         part = music21.stream.Part()
#         part.id = name_part
#         parts.append(part)
#
#     part = parts[0]
#
#     df_grans['event'] = (df_grans['melody'].shift(1) != df_grans['melody']).astype(int).cumsum()
#
#     df_events = df_grans.reset_index().groupby(['melody','event'])[column_index].apply(np.array)
#
#     beat_to_note = dict()
#
#     for i, span in df_events.iteritems():
#         pitch_midi = i[0]
#         beat_start = span[0]
#         beat_end = span[-1]
#         duration = beat_end - beat_start + 1/48
#
#         duration = music21.duration.Duration(duration)
#
#         if not pitch_midi > 0:
#             note = music21.note.Rest(duration=duration)
#         else:
#             note = music21.note.Note(pitch=music21.pitch.Pitch(midi=int(pitch_midi)), duration=duration)
#
#         beat_to_note[beat_start] = note
#
#     measure = music21.stream.Measure()
#
#     for beat in df_grans.index.get_level_values(0).tolist():
#         if int(beat) == beat and int(beat) % 4 == 0:
#             part.append(measure)
#             measure = music21.stream.Measure()
#
#         if beat in beat_to_note:
#             note = beat_to_note[beat]
#             measure.append(
#                 note
#             )
#
#     score = music21.stream.Score()
#
#     score.insert(0, part)
#
#     return score

