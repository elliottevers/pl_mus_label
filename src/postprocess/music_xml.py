import pandas as pd
import music21


# def smooth_chords(df: pd.DataFrame) -> pd.DataFrame:
#     return


def get_lowest_note(chord):
    return list(chord.pitches)[0]


def get_highest_notes(chord):
    if not chord:
        return None
    else:
        return music21.chord.Chord(
            list(chord.pitches)[1:]
        )


def extract_bass(df_chords) -> pd.DataFrame:
    return df_chords['chord'].apply(get_lowest_note).to_frame(name='bass')


def extract_upper_voices(df_chords) -> pd.DataFrame:
    return df_chords['chord'].apply(get_highest_notes).to_frame(name='chord')

