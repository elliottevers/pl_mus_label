import pandas as pd
import music21
import numpy as np
from live import note as nl
from typing import List, Dict, Any, Optional, Tuple
from itertools import groupby
from fractions import Fraction
import math
from utils import utils
import json


def from_json(filepath, parts=['melody', 'chord', 'bass']) -> music21.stream.Score:

    with open(filepath) as f:
        json_read = json.load(f)

    partmap = {}

    # beat_length_score = json_read['length_beats']

    for name_part in utils.intersection(parts, list(json_read.keys())):
        part = music21.stream.Part()

        notes = nl.NoteLive.parse_list(
            json_read[name_part]['notes']
        )

        for note_live in notes:

            note = note.Note(
                pitch=note_live.pitch
            )
            note.duration = music21.duration.Duration(
                note_live.beats_duration
            )

            part.insert(
                note_live.beat_start,
                note
            )

        if name_part == 'chord':
            part.makeVoices()

        part.makeRests(fillGaps=True)

        part.makeMeasures()

        part.id = name_part

        part.partName = name_part

        partmap[name_part] = part

    score = music21.stream.Score()

    for _, part in partmap.items():
        score.append(part)

    return score


def get_lowest_note(chord):
    return list(chord.pitches)[0]


def get_highest_notes(chord_local):
    if not chord_local:
        return None
    else:
        return music21.chord.Chord(
            list(chord_local.pitches)[1:]
        )


def extract_bass(df_chords) -> pd.DataFrame:
    return df_chords['chord'].apply(get_lowest_note).to_frame(name='bass')


def extract_upper_voices(df_chords) -> pd.DataFrame:
    return df_chords['chord'].apply(get_highest_notes).to_frame(name='chord')


def extract_upper_voices_stream(stream) -> music21.stream.Part:
    part_upper = music21.stream.Part()
    part_upper.id = 'chord'

    for obj in stream:
        offset = obj.offset
        duration = obj.duration
        if isinstance(obj, music21.chord.Chord):
            obj = music21.chord.Chord(
                obj.pitches[1:],
                duration=duration
            )

        part_upper.insert(offset, obj)

    return part_upper


def extract_parts(score: music21.stream.Score, parts=['chord', 'bass']) -> music21.stream.Score:
    score_diminished = music21.stream.Score()

    for i_part, name_part in enumerate(parts):
        score_diminished.insert(i_part, extract_part(score, name_part))

    return score_diminished


def extract_part(score: music21.stream.Score, name_part):  #   -> stream.Part:
    return score.getElementById(name_part)


def add_part(part: music21.stream.Part, score: music21.stream.Score, id='key_center') -> music21.stream.Score:
    part.id = id
    score.insert(
        len(score.elements),
        part
    )
    return score


# def freeze_stream(stream, filepath) -> None:
#     stream_frozen = freezeThaw.StreamFreezer(stream)
#     stream_frozen.write(fmt='pickle', fp=filepath)
#
#
# def thaw_stream(filepath) -> stream.Stream:
#     thawer = freezeThaw.StreamThawer()
#     thawer.open(fp=filepath)
#     return thawer.stream


def set_tempo(score: music21.stream.Score, bpm: int = 60) -> music21.stream.Score:

    marks_to_remove = []

    # remove current
    for mark in score.flat.getElementsByClass(music21.tempo.MetronomeMark):
        marks_to_remove.append(mark)

    for mark in marks_to_remove:
        score.remove(mark, recurse=True)

    # add new
    for measure in score.parts[0].getElementsByClass(music21.stream.Measure):
        if measure.offset == 0.0:
            tempo = tempo.MetronomeMark(number=bpm)
            tempo.offset = 0.0
            measure.append(tempo)

    return score


def get_struct_score(object, name_part, dur):
    if name_part == 'melody':
        if not object > 0:
            struct_score = music21.note.Rest()
        else:
            struct_score = music21.note.Note(
                pitch=music21.pitch.Pitch(
                    midi=int(object)
                )
            )
    elif name_part == 'chord':
        if not object:
            struct_score = music21.note.Rest()
        else:
            struct_score = music21.chord.fromIntervalVector(
                object
            )

    elif name_part == 'bass':
        struct_score = music21.note.Note(
            pitch=object
        )
    elif name_part == 'segment':
        struct_score = music21.note.Note(
            pitch=music21.pitch.Pitch(
                midi=60
            )
        )
    else:
        raise 'part ' + name_part + ' not in dataframe to render to score'

    struct_score.duration = dur

    return struct_score


# def to_diff(df: pd.DataFrame, name_column='melody', sample_rate=0.003) -> pd.DataFrame:
#     offset_diff = []
#     data_diff = []
#     duration_diff = []
#
#     current_val = None
#
#     acc_duration = 0
#
#     # resolution_beats = 48
#
#     for i, val in df[name_column].iteritems():
#         acc_duration = acc_duration + sample_rate
#         if val == current_val:
#             pass
#         else:
#             offset_diff.append(i)
#             data_diff.append(val)
#             duration_diff.append(acc_duration)
#             acc_duration = 0
#             current_val = val
#
#     df_diff = pd.DataFrame(
#         data={
#             name_column: data_diff,
#             get_name_column_duration(name_column): duration_diff
#         },
#         index=offset_diff
#     )
#
#     df_diff.index.name = get_name_column_offset(name_column)
#
#     return df_diff


# def df_grans_quantized_to_score(
#         df_grans: pd.DataFrame,
#         parts=[
#             'melody',
#             'chord',
#             'bass',
#             'segment'
#         ],
#         resolution_measure=48
# ) -> stream.Score:
#
#     score = stream.Score()
#
#     for i_part, name_part in enumerate(parts):
#
#         part = stream.Part()
#
#         part.id = name_part
#
#         counter_measure = 1
#
#         measure = stream.Measure(
#             number=counter_measure
#         )
#
#         acc_duration = 0
#
#         for row in df_grans.itertuples():
#             index = row[0]
#             index_beat_offset = index[0]
#             obj = row[1]
#             duration = row[2]
#
#             duration_to_nearest_gran = Fraction(int(round(resolution_measure * duration)), resolution_measure)
#             beat_offset_to_nearest_gran = Fraction(int(round(resolution_measure * index_beat_offset)), resolution_measure)
#
#             if int(acc_duration) > 0 and int(acc_duration) % 4 == 0:
#                 part.append(measure)
#                 counter_measure = counter_measure + 1
#                 measure = stream.Measure(
#                     number=counter_measure
#                 )
#                 acc_duration = 0
#
#             struct_score = get_struct_score(obj, name_part)
#             struct_score.duration = duration.Duration(duration_to_nearest_gran)
#             measure.append(struct_score)
#             acc_duration = acc_duration + duration_to_nearest_gran
#
#
#         score.insert(i_part, part)
#
#     return score


def df_grans_to_score(
        df_grans: pd.DataFrame,
        # column_index='beat',
        parts=[
            'melody',
            'chord',
            'bass',
            'segment'
        ]
) -> music21.stream.Score:

    score = music21.stream.Score()

    for i_part, name_part in enumerate(parts):

        part = music21.stream.Part()

        part.id = name_part

        obj_first = df_grans.loc[df_grans.index[0]][0]

        offset_first = df_grans.index[0][0]

        counter = 0

        obj_last = obj_first

        offset_last = offset_first

        for row in df_grans.itertuples():

            counter = counter + 1

            if counter == 1:
                continue

            index = row[0]
            index_beat = index[0]
            obj = row[1]

            if obj != obj_last:

                dur = music21.duration.Duration(index_beat - offset_last)

                offset = offset_last

                part.insert(
                    offset,
                    get_struct_score(
                        obj_last,
                        name_part,
                        dur
                    )
                )

                obj_last = obj

                offset_last = index_beat

        score.insert(i_part, part)

    return score


# TODO: replace
def live_to_stream(
        notes_live: List[nl.NoteLive],
        mode: str = 'monophonic'
) -> music21.stream.Part:

    part = music21.stream.Part()

    if mode == 'monophonic':

        for note_live in notes_live:
            note = music21.note.Note(
                pitch=note_live.pitch
            )
            note.duration = music21.duration.Duration(
                note_live.beats_duration
            )

            part.insert(note_live.beat_start, note)

    elif mode == 'polyphonic':
        # TODO: this hard a hard requirement that they're sorted by beat beforehand
        groups_notes = []
        unique_onsets_beats = []

        def get_beat_start(note):
            return note.beat_start

        for beat_start, group_note in groupby(notes_live, get_beat_start):
            groups_notes.append(list(group_note))
            unique_onsets_beats.append(beat_start)

        for group in groups_notes:

            chord = music21.chord.Chord([
                music21.note.Note(
                    pitch=music21.pitch.Pitch(
                        midi=note_live.pitch
                    )
                ).name for
                note_live
                in group
            ])

            # TODO: this makes the assumption that all notes in the group have the same offsets and duration

            chord.duration = music21.duration.Duration(group[-1].beats_duration)

            part.insert(group[-1].beat_start, chord)

    else:
        raise 'mode ' + mode + 'not supported'

    return part

