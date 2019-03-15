from typing import List, Dict, Any, Optional, Tuple
# from music import note as lib_note, chord as lib_chord
# from music21 import harmony, chord
import music21


def vamp_chord_to_dict(s_to_label_chords: List[Dict[float, Any]]) -> Dict[float, music21.chord.Chord]:

    events_chords = dict()

    for event in s_to_label_chords:

        event_non_slash = event['label'].split('/', 1)[0]

        if len(event_non_slash) > 1 and event_non_slash[1] == 'b':
            event_non_slash = list(event_non_slash)
            event_non_slash[1] = '-'
            event_non_slash = ''.join(event_non_slash)

        chord_realized = music21.harmony.ChordSymbol(event_non_slash)

        chord_midi = music21.chord.Chord(
            notes=[
                pitch.name for pitch in chord_realized.pitches
            ]
        )

        events_chords[event['timestamp']] = chord_midi

    return events_chords
