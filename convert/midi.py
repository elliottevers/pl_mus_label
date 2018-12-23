import pandas as pd
from typing import List, Dict
import math
import mido


# def filter_length(
#         divisor_quarter_note,
#         track_to_filter,
#         ppq,
#         bpm
# ):

def mid_to_series(
        track
):

    # track = MidiTrack()
    #
    # track.append(
    #     MetaMessage(
    #         'time_signature',
    #         time=0
    #     )
    # )
    #
    # track.append(
    #     MetaMessage(
    #         'set_tempo',
    #         tempo=mido.bpm2tempo(bpm),
    #         time=0
    #     )
    # )

    # len_note_filter = ppq / divisor_quarter_note

    iter_tick = 0

    tick_last = 0

    ticks = []

    notes_midi = []

    notes_intervals_tick: List[Dict[int, List]] = []

    for msg in track:
        if msg.type == 'note_on':
            # ticks_since_onset_last = int(round(mido.second2tick(msg.time, ppq, mido.bpm2tempo(bpm))))
            ticks_since_onset_last = msg.time
            # track.append(Message('note_on', note=msg.note, velocity=msg.velocity, time=ticks_since_onset_last))
            for tick_empty in range(ticks_since_onset_last):
                # counting ticks during 'note_off' messages
                iter_tick += 1
                ticks.append(tick_last + tick_empty)
                notes_midi.append(None)

        if msg.type == 'note_off':
            # ticks_since_onset_last = int(round(mido.second2tick(msg.time, ppq, mido.bpm2tempo(bpm))))
            ticks_since_onset_last = msg.time
            # track.append(Message('note_off', note=msg.note, velocity=msg.velocity, time=ticks_since_onset_last))
            interval = []
            interval.append(iter_tick + 1)
            for tick in range(ticks_since_onset_last):
                # counting ticks during 'note_on' messages
                iter_tick += 1
                ticks.append(tick_last + tick)
                notes_midi.append(msg.note)

            interval.append(iter_tick)
            notes_intervals_tick.append({msg.note: interval})
        tick_last = iter_tick

    return pd.Series(
        notes_midi,
        index=ticks
    ), notes_intervals_tick


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
