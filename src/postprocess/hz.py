import pandas as pd
import math
import librosa


def _handle_na(h):
    return 0 if not h or math.isinf(h) or math.isnan(h) or h < 0 else int(h)


# TODO: does this already do a diff?
def midify(df: pd.DataFrame):
    return df.apply(_handle_na).diff(1).cumsum().apply(librosa.hz_to_midi).round().apply(_handle_na)

