import numpy as np


def to_coll(df, filename):
    df['pos'] = np.arange(len(df))
    df['pos'] = df['pos'] + 1
    df_coll = df[['pos', 'melody']]
    df_coll[df_coll.columns[-1]] = df_coll[df_coll.columns[-1]].astype(str).map(lambda entry: entry + ';')
    df_coll.to_csv(
        filename,
        header=None,
        columns=['pos', 'melody'],
        index=False
    )
