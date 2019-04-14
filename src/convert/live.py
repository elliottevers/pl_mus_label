import pandas as pd


def with_index_live(df: pd.DataFrame) -> pd.DataFrame:
    df.index = pd.MultiIndex.from_tuples([(x[0] - 1, x[1]) for x in df.index])
    return df
