import music21
from live import note as nl
from typing import List, Dict, Tuple
from quantize import mesh
from itertools import groupby
from fractions import Fraction


def live_to_stream(
        notes_live: List[nl.NoteLive],
        beatmap: List[float],
        s_beat_start: float,
        s_beat_end: float,
        tempo: float,
        mode: str = 'monophonic',
) -> music21.stream.Part:

    part = music21.stream.Part()

    gran_map = mesh.MeshScore.get_gran_map(
        mesh.MeshScore.trim_beatmap(beatmap, s_beat_start, s_beat_end)
    )

    if mode == 'monophonic':

        for note_live in notes_live:
            note = music21.note.Note(
                pitch=note_live.pitch
            )

            offset_start = second_to_offset(
                beat_to_second(
                    note_live.beat_start,
                    tempo_bpm=tempo
                ),
                gran_map=gran_map
            )

            note.duration = music21.duration.Duration(
                _get_duration_granule(note_live.beats_duration)
            )

            part.insert(
                _get_duration_granule(offset_start),
                note
            )

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
                note_live.pitch for
                note_live
                in group
            ])

            # TODO: this makes the assumption that all notes in the group have the same offsets and duration

            chord.duration = music21.duration.Duration(
                _get_duration_granule(group[-1].beats_duration)
            )

            offset_start = second_to_offset(
                beat_to_second(
                    group[-1].beat_start,
                    tempo_bpm=tempo
                ),
                gran_map=gran_map
            )

            part.insert(
                _get_duration_granule(offset_start),
                chord
            )

    else:
        raise 'mode ' + mode + 'not supported'

    return part


def _get_duration_granule(duration):
    return Fraction(int(round(48 * duration)), 48)


def second_to_beat(second: int, tempo_bpm: int) -> float:
    tempo_bps = tempo_bpm/60
    return float(tempo_bps * second)


def offset_to_second(offset: float, gran_map: Dict[float, float]):
    beat_nearest, s_nearest = min(list(gran_map.items()), key=lambda pair: abs(pair[0] - float(offset)))
    return s_nearest


def beat_to_second(beat: float, tempo_bpm: float) -> float:
    tempo_bps = tempo_bpm/60
    return float(beat/tempo_bps)


def second_to_offset(second: float, gran_map: Dict[float, float]) -> float:
    beat_nearest, s_nearest = min(list(gran_map.items()), key=lambda pair: abs(pair[1] - float(second)))
    return beat_nearest


def to_note_live(
        note_21,
        tempo,
        gran_map
):
    beat_offset = second_to_beat(
        offset_to_second(
            float(note_21.offset),
            gran_map
        ),
        tempo
    )

    return nl.NoteLive(
        pitch=int(note_21.pitch.midi),
        beat_start=float(beat_offset),
        beats_duration=float(note_21.duration.quarterLength),
        velocity=90,
        muted=0
    )


def to_notes_live(
        stream: music21.stream.Stream,
        beatmap: List[int],
        s_beat_start: int,
        s_beat_end: int,
        tempo: int
):

    gran_map = mesh.MeshScore.get_gran_map(
        mesh.MeshScore.trim_beatmap(beatmap, s_beat_start, s_beat_end)
    )

    notes_live = []

    for struct_21 in stream:

        if isinstance(struct_21, music21.stream.Measure):
            for note in struct_21:
                note_absolute_offset = note
                # NB: a note's offset is relative to the measure that contains it
                note_absolute_offset.offset = struct_21.offset + note.offset
                notes_live.append(
                    to_note_live(
                        note_absolute_offset,
                        tempo=tempo,
                        gran_map=gran_map
                    )
                )

        if isinstance(struct_21, music21.note.Note):
            notes_live.append(
                to_note_live(
                    struct_21,
                    tempo=tempo,
                    gran_map=gran_map
                )
            )

        if isinstance(struct_21, music21.chord.Chord):
            offset = struct_21.offset
            duration = struct_21.duration
            for pitch in struct_21.pitches:
                note = music21.note.Note(
                    pitch=pitch.midi,
                    duration=duration
                )
                note.offset = offset
                notes_live.append(
                    to_note_live(
                        note,
                        tempo=tempo,
                        gran_map=gran_map
                    )
                )

    return notes_live
