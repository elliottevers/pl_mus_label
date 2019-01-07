import pandas as pd
from typing import List, Dict
import math
import mido


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
            # ticks_since_onset_last = int(round(mido.second2tick(msg.time, ppq, mido.bpm2tempo(bpm))))
            ticks_since_onset_last = msg.time
            # track.append(Message('note_on', note=msg.note, velocity=msg.velocity, time=ticks_since_onset_last))
            for tick_empty in range(ticks_since_onset_last):
                # counting ticks during 'note_off' messages
                iter_tick += 1
                ticks.append(tick_last + tick_empty)
                # notes_midi.append(note_current if last_msg_type_note_on else None)
                notes_midi.append(stack_note_sounding[-1])
            # note_current = stack_note_sounding[-1]
            # last_msg_type_note_on = True
            stack_note_sounding.append(note)

        if msg.type == 'note_off':
            note = int(msg.note)
            # if stack_note_sounding[-1] == note:

            # ticks_since_onset_last = int(round(mido.second2tick(msg.time, ppq, mido.bpm2tempo(bpm))))
            ticks_since_onset_last = msg.time
            # track.append(Message('note_off', note=msg.note, velocity=msg.velocity, time=ticks_since_onset_last))
            interval = [iter_tick + 1]
            # interval.append(iter_tick + 1)
            for tick in range(ticks_since_onset_last):
                # counting ticks during 'note_on' messages
                iter_tick += 1
                ticks.append(tick_last + tick)
                notes_midi.append(stack_note_sounding[-1])  # notes_midi.append(note)

            interval.append(iter_tick)
            notes_intervals_tick.append({stack_note_sounding[-1]: interval})
            if stack_note_sounding[-1] == note:
                stack_note_sounding.pop()
            # note_last = note
            # last_msg_type_note_on = False

        tick_last = iter_tick

    # assert stack_note_sounding[-1] is None
    ticks.append(tick_last)
    # notes_midi.append(stack_note_sounding[-1])
    notes_midi.append(None)

    return pd.Series(
        notes_midi,
        index=ticks
    )  #  , notes_intervals_tick


def series_to_mid(df, init_velocity):

    iter_tick = 0

    onset_tick = 0

    note_last = 0

    track = mido.MidiTrack()

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
                mido.Message(
                    'note_off',
                    note=note_last,
                    velocity=0,
                    time=int(tick_next - onset_tick)
                )
            )

            track.append(
                mido.Message(
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