import math
import mido


def timeseries_ticks_to_mid(df, track, init_velocity):

    iter_tick = 0

    onset_tick = 0

    note_last = 0

    while iter_tick < len(df) - 1:

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
