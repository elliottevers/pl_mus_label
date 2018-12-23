import mido
from mido import Message, MetaMessage, MidiTrack
import pandas as pd


# def filter_length(
#         divisor_quarter_note,
#         track_to_filter,
#         ppq,
#         bpm
# ):

def mid_to_series(
        track
):

    track = MidiTrack()

    track.append(
        MetaMessage(
            'time_signature',
            time=0
        )
    )

    track.append(
        MetaMessage(
            'set_tempo',
            tempo=mido.bpm2tempo(bpm),
            time=0
        )
    )

    len_note_filter = ppq / divisor_quarter_note

    iter_tick = 0

    tick_last = 0

    ticks = []

    notes_midi = []

    boundaries_notes

    for msg in track_to_filter:
        if msg.type == 'note_on':
            ticks_since_onset_last = int(round(mido.second2tick(msg.time, ppq, mido.bpm2tempo(bpm))))
            track.append(Message('note_on', note=msg.note, velocity=msg.velocity, time=ticks_since_onset_last))
            for tick_empty in range(ticks_since_onset_last):
                # counting ticks during 'note_off' messages
                iter_tick += 1
                ticks.append(tick_last + tick_empty)
                notes_midi.append(None)

        if msg.type == 'note_off':
            ticks_since_onset_last = int(round(mido.second2tick(msg.time, ppq, mido.bpm2tempo(bpm))))
            track.append(Message('note_off', note=msg.note, velocity=msg.velocity, time=ticks_since_onset_last))
            for tick in range(ticks_since_onset_last):
                # counting ticks during 'note_on' messages
                iter_tick += 1
                ticks.append(tick_last + tick)
                # Filter out notes
                # if ticks_since_onset_last < len_note_filter:
                #     notes_midi.append(None)
                # else:
                #     notes_midi.append(msg.note)

        tick_last = iter_tick

    return pd.Series(
        notes_midi,
        index=ticks
    ), notes_boundaries
