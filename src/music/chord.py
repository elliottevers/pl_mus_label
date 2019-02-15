from music import note
from typing import List, Dict, Any, Optional, Tuple


class ChordMidi(object):
    def __init__(self, notes: List[note.MidiNote]):
        self.notes = notes

    def __eq__(self, other):
        return [note.pitch for note in self.notes] == [note.pitch for note in other.notes]
