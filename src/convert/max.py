import librosa
import pandas as pd
from postprocess import hz as hz_postp


def hz_to_mid(hz):
    if hz == 0:
        return 0
    else:
        return librosa.hz_to_midi(hz)

# TODO: convert to midi before diffing, create rests where pitch is 0


def to_mid(df_hz: pd.DataFrame, name_part):
    df_hz[name_part] = df_hz[name_part].apply(hz_postp._handle_na).apply(hz_to_mid).apply(round)
    return df_hz
