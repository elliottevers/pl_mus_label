

def filter_note_length(
        df,
        boundaries_notes,
        divisor_quarter_note=1,
        ppq=1000
):
    len_filter_note_ticks = ppq/divisor_quarter_note

    # df.loc[0:len(df.index)] = 0

    for pitch, bounds in [(pitch, bounds) for note in boundaries_notes for (pitch, bounds) in note.items()]:
        if bounds[1] - bounds[0] < len_filter_note_ticks:
            df.loc[bounds[0]:bounds[1]] = None

    return df
