from typing import List, Dict, Any, Optional, Tuple
from music import note as lib_note, chord as lib_chord
from music21 import harmony


def vamp_to_dict(s_to_label_chords: List[Dict[float, Any]], type_index='s') -> Dict[float, lib_chord.ChordMidi]:

    events_chords = dict()

    for chord in s_to_label_chords:
        duration_ticks = None  # TODO: calculate here, instead of during midi file creation
        velocity = 90
        chord_realized = harmony.ChordSymbol(chord['label'].replace('b', '-'))
        # TODO: keeping to_float() is a necessity for vamp conversion
        # events_chords[chord['timestamp'].to_float()] = [
        #     note.MidiNote(pitch.midi, duration_ticks, velocity) for pitch in chord_realized.pitches
        # ]
        chord_midi = lib_chord.ChordMidi(
            notes=[
                lib_note.MidiNote(pitch.midi, duration_ticks, velocity) for pitch in chord_realized.pitches
            ]
        )
        events_chords[chord['timestamp']] = chord_midi

    return events_chords
