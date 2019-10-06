import librosa
import pandas as pd
from postprocess import hz as hz_postp
import numpy as np


file_ts_coll = '/Users/elliottevers/Documents/git-repos.nosync/tk_music_projects/ts_hz.txt'

file_ts_coll_discrete = '/Users/elliottevers/Documents/git-repos.nosync/tk_music_projects/ts_hz_discretized.txt'


def hz_to_mid(hz):
    if hz == 0:
        return 0
    else:
        return librosa.hz_to_midi(hz)

# TODO: convert to midi before diffing, create rests where pitch is 0


def to_mid(df_hz: pd.DataFrame, name_part):
    df_hz[name_part] = df_hz[name_part].apply(hz_postp._handle_na).apply(hz_to_mid).apply(round)
    return df_hz


def to_coll(df, filename):
    df['pos'] = np.arange(len(df))
    df['pos'] = df['pos'] + 1
    df_coll = df[['pos', 'signal']]
    df_coll[df_coll.columns[-1]] = df_coll[df_coll.columns[-1]].astype(str).map(lambda entry: entry + ';')
    df_coll.to_csv(
        filename,
        header=None,
        columns=['pos', 'signal'],
        index=False
    )


def from_coll(filename):
    df = pd.read_csv(
        filename,
        header=None,
        names=['pos', 'signal']
    )

    # get rid of semi-colons at end
    df['signal'] = df['signal'].map(lambda line: line.rstrip(';')).astype(np.float)

    return df
