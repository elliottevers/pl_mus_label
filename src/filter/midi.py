import mido
from mido import Message, MetaMessage, MidiTrack
import pandas as pd
import itertools
from music import song


def get_name_column_duration(name_column):
    return name_column + '_duration'


def get_name_column_offset(name_column):
    return name_column + '_offset'


def to_diff(df: pd.DataFrame, name_column='melody', sample_rate=0.003) -> pd.DataFrame:
    offset_diff = []
    data_diff = []
    duration_diff = []

    current_val = None

    acc_duration = 0

    for i, val in df[name_column].iteritems():
        acc_duration = acc_duration + sample_rate
        if val == current_val:
            pass
        else:
            offset_diff.append(i)
            data_diff.append(val)
            duration_diff.append(acc_duration)
            acc_duration = 0
            current_val = val

    df_diff = pd.DataFrame(
        data={
            name_column: data_diff,
            get_name_column_duration(name_column): duration_diff
        },
        index=offset_diff
    )

    df_diff.index.name = get_name_column_offset(name_column)

    return df_diff


# df of music21 object that know they're duration, and the index knows it's offset
def to_df_beat_unquantized(df_diff, name_column, beatmap, beat_first, beat_last):
    # TODO: partmap

    beatmap_trimmed = song.MeshSong.trim_beatmap(beatmap, beat_first, beat_last)

    def find_index_of_nearest_below(array, value):
        return array.index(max(list(filter(lambda y: y <= 0, [x - value for x in array]))) + value)

    def to_beat_onset(ms, beatmap, index_nearest_below, length_containing_segment):
        nearest_below = beatmap[index_nearest_below]

        return beatmap.index(nearest_below) + (
            (ms - beatmap[index_nearest_below])/length_containing_segment
        )

    index_beat_offset = []
    data_beat_duration = []
    data_struct = []

    for row in df_diff.itertuples(index=True, name=True):
        index_s_offset = row[0]
        struct = row[1]
        s_duration = row[2]

        if index_s_offset < beatmap_trimmed[0] or index_s_offset > beatmap_trimmed[-1]:
            continue

        index_nearest_below = find_index_of_nearest_below(beatmap_trimmed, index_s_offset)
        length_of_containing_segment = beatmap_trimmed[index_nearest_below + 1] - beatmap_trimmed[index_nearest_below]
        beat_onset = to_beat_onset(index_s_offset, beatmap_trimmed, index_nearest_below, length_of_containing_segment)
        beat_duration = s_duration/length_of_containing_segment

        index_beat_offset.append(beat_onset)
        data_beat_duration.append(beat_duration)
        data_struct.append(struct)

    df_struct = pd.DataFrame(
        data={
            name_column: data_struct,
            get_name_column_duration(name_column): data_beat_duration
        },
        index=index_beat_offset
    )

    df_struct.index.name = 'beat'

    return df_struct


# def pad(
#     track,
#     bpm,
#     num_copies=2
# ):
#
#     track_padded = mido.MidiTrack()
#
#     track_padded.append(
#         MetaMessage(
#             'time_signature',
#             time=0
#         )
#     )
#
#     track_padded.append(
#         MetaMessage(
#             'set_tempo',
#             tempo=mido.bpm2tempo(bpm),
#             time=0
#         )
#     )
#
#     for _ in itertools.repeat(None, num_copies):
#         for msg in track:
#             if not msg.is_meta:
#                 track_padded.append(msg)
#
#     return track_padded


#
# def smooth_chords(df: pd.DataFrame, cadence_beats=4) -> pd.DataFrame:
#     chords_smoothed = []
#
#     # NB: we assume here that the first level of index is "beat"
#     for index, row in df.itertuples(index=True, name='chord'):
#         if index[0] % 4 == 1:
#             chords_smoothed.append(df.loc[(index[0] + 1, slice(None)), 'chord'].values[0])
#         elif index[0] % 4 == 0:
#             chords_smoothed.append(df.loc[(index[0] - 1, slice(None)), 'chord'].values[0])
#         else:
#             chords_smoothed.append(df.loc[(index[0], slice(None)), 'chord'].values[0])
#
#     df_smoothed = df
#     df_smoothed['chord'] = chords_smoothed
#     return df_smoothed


# def smooth_bass(df: pd.DataFrame, cadence_beats=1) -> pd.DataFrame:
#     bass_smoothed = []
#
#     for index, row in df.itertuples(index=True, name='bass'):
#         if index[0] % 4 == 1:
#             bass_smoothed.append(df.loc[(index[0] + 1, slice(None)), 'bass'].values[0])
#         elif index[0] % 4 == 0:
#             bass_smoothed.append(df.loc[(index[0] - 1, slice(None)), 'bass'].values[0])
#         else:
#             bass_smoothed.append(df.loc[(index[0], slice(None)), 'bass'].values[0])
#
#     df_smoothed = df
#     df_smoothed['bass'] = bass_smoothed
#     return df_smoothed


# def smooth_segment(df: pd.DataFrame, cadence_beats=16) -> pd.DataFrame:
#     segment_smoothed = []
#
#     for index, row in df.itertuples(index=True, name='segment'):
#         if index[0] % 4 == 1:
#             segment_smoothed.append(df.loc[(index[0] + 1, slice(None)), 'segment'].values[0])
#         elif index[0] % 4 == 0:
#             segment_smoothed.append(df.loc[(index[0] - 1, slice(None)), 'segment'].values[0])
#         else:
#             segment_smoothed.append(df.loc[(index[0], slice(None)), 'segment'].values[0])
#
#     df_smoothed = df
#     df_smoothed['segment'] = segment_smoothed
#     return df_smoothed

