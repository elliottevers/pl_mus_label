from typing import List, Dict, Any


def filter_non_chords(s_to_label_chords: List[Dict[float, Any]]) -> List[Dict[float, Any]]:
    return list(filter(lambda event_chord: event_chord['label'] != 'N', s_to_label_chords))

