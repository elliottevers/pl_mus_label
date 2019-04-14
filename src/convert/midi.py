import pandas as pd
from typing import List, Dict
import math
from mido import MidiTrack, Message, MetaMessage, bpm2tempo
import librosa


def df_to_mid(df, label_part, index='s', bpm=60, ppq=1000, program=22) -> MidiTrack:

    track = MidiTrack()

    track.append(
        Message(
            'program_change',
            program=program,
            time=0
        )
    )

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

    index_seconds = df.index.get_level_values(1)

    time_s_last = list(index_seconds)[0]

    df.loc[(slice(None), index_seconds[1:]), :]['chord'].tolist()

    df.loc[(slice(None), index_seconds[1:]), :]['chord'].tolist()

    for time_s in list(index_seconds):

        diff_ticks_last_event = s_to_ticks(time_s, bpm=bpm, ppq=ppq) - s_to_ticks(time_s_last, bpm=bpm, ppq=ppq)

        for i_note, note in enumerate(df.loc[(slice(None), time_s_last), 'chord'].tolist()[0]):
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

        for i_note, note in enumerate(df.loc[(slice(None), time_s), 'chord'].tolist()[0]):
            track.append(
                Message(
                    'note_on',
                    note=note.pitch,
                    velocity=note.velocity,
                    time=0
                )
            )

        time_s_last = time_s

    return track


def s_to_ticks(s, bpm=60, ppq=480):

    quarter_notes_per_minute = bpm

    ticks_per_quarter_note = ppq

    ms_per_minute = (60 * 1000)

    ticks_per_minute = ticks_per_quarter_note * quarter_notes_per_minute

    ticks_per_ms = ticks_per_minute / ms_per_minute

    ms_per_second = 1000

    return int(ticks_per_ms * ms_per_second * s)


def mid_to_series(
        track
):

    iter_tick = 0

    tick_last = 0

    ticks = []

    notes_midi = []

    notes_intervals_tick: List[Dict[int, List]] = []

    last_msg_type_note_on = False

    stack_note_sounding = [None]

    for msg in track:
        if msg.type == 'note_on':

            note = int(msg.note)
            ticks_since_onset_last = msg.time

            for tick_empty in range(ticks_since_onset_last):
                # counting ticks during 'note_off' messages
                iter_tick += 1
                ticks.append(tick_last + tick_empty)
                notes_midi.append(stack_note_sounding[-1])

            stack_note_sounding.append(note)

        if msg.type == 'note_off':
            note = int(msg.note)

            ticks_since_onset_last = msg.time
            interval = [iter_tick + 1]

            for tick in range(ticks_since_onset_last):
                # counting ticks during 'note_on' messages
                iter_tick += 1
                ticks.append(tick_last + tick)
                notes_midi.append(stack_note_sounding[-1])  # notes_midi.append(note)

            interval.append(iter_tick)
            notes_intervals_tick.append({stack_note_sounding[-1]: interval})
            if stack_note_sounding[-1] == note:
                stack_note_sounding.pop()

        tick_last = iter_tick

    ticks.append(tick_last)
    notes_midi.append(None)

    return pd.Series(
        notes_midi,
        index=ticks
    )


def series_to_mid(df, init_velocity):

    iter_tick = 0

    onset_tick = 0

    note_last = 0

    track = MidiTrack()

    while iter_tick < len(df.index) - 1:

        velocity = init_velocity

        tick_next = iter_tick + 1

        pitch_current = df.at[iter_tick]

        pitch_next = df.at[tick_next]

        if pitch_current != pitch_next and not (math.isnan(pitch_current) and math.isnan(pitch_next)):

            note = int(df.at[tick_next]) if df.at[tick_next] > 0 else 0

            if note == 0:
                velocity = 0

            track.append(
                Message(
                    'note_off',
                    note=note_last,
                    velocity=0,
                    time=int(tick_next - onset_tick)
                )
            )

            track.append(
                Message(
                    'note_on',
                    note=note,
                    velocity=int(velocity),
                    time=0
                )
            )

            if velocity > 0:
                note_last = note

            onset_tick = iter_tick + 1

        iter_tick = tick_next

    return track


def hz_to_mid(
        df_hz: pd.DataFrame
) -> pd.DataFrame:
    df_hz['melody'] = df_hz['melody'].apply(librosa.hz_to_midi).round()
    return df_hz
