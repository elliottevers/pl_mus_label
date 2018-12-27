import mido
from mido import Message, MetaMessage, MidiTrack
import pandas as pd
import itertools


# def filter_length(
#         divisor_quarter_note,
#         track_to_filter,
#         ppq,
#         bpm
# ):

def pad(
    track,
    bpm,
    num_copies=2
):

    track_padded = mido.MidiTrack()

    track_padded.append(
        MetaMessage(
            'time_signature',
            time=0
        )
    )

    track_padded.append(
        MetaMessage(
            'set_tempo',
            tempo=mido.bpm2tempo(bpm),
            time=0
        )
    )

    for _ in itertools.repeat(None, num_copies):
        for msg in track:
            if not msg.is_meta:
                track_padded.append(msg)

    return track_padded

