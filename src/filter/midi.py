import pandas as pd
from quantize import mesh


def get_name_column_duration(name_column):
    return name_column + '_duration'


def get_name_column_offset(name_column):
    return name_column + '_offset'


def to_diff(df: pd.DataFrame, name_column='melody', sample_rate=0.0029) -> pd.DataFrame:
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
            data_diff.append(current_val)
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

    beatmap_trimmed = mesh.MeshScore.trim_beatmap(beatmap, beat_first, beat_last)

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
