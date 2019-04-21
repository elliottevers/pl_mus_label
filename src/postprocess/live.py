

def filter_empty(notes_live):
    return list(filter(lambda note: note.beats_duration > 0, notes_live))
