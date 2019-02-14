from typing import List, Dict, Any, Optional, Tuple
from music import note


Beat = int

IntervalBeat = [Beat, Beat]


class Segment(object):
    def __init__(self, interval: IntervalBeat, instrument='cymbals'):
        self.realization = note.MidiNote()
