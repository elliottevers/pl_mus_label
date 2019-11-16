import pandas as pd


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
            _get_name_column_duration(name_column): duration_diff
        },
        index=offset_diff
    )

    df_diff.index.name = _get_name_column_offset(name_column)

    return df_diff


def _get_name_column_duration(name_column):
    return name_column + '_duration'


def _get_name_column_offset(name_column):
    return name_column + '_offset'
