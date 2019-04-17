from typing import List, Dict, Any, Optional, Tuple
import music21
import numpy as np
from utils import utils
import librosa


def to_data_monophonic(data_midi, offset_s_audio, duration_s_audio, beatmap, sample_rate=.0029):

    data = list()

    data.append(sample_rate)

    space_sample = np.zeros(int(duration_s_audio/sample_rate) + 1)

    def beat_to_second(beat):
        return beatmap[int(beat)] + (beatmap[int(beat) + 1] - beatmap[int(beat)])*(float(beat) - int(beat))

    def second_to_index(s, array):
        return int(s / duration_s_audio * len(array))

    for note in data_midi:
        offset_i_note = second_to_index(beat_to_second(note.beat_start), space_sample)
        duration_i_note = second_to_index(beat_to_second(note.beats_duration), space_sample)
        idx = list(range(offset_i_note, offset_i_note + duration_i_note))
        space_sample[list(filter(lambda x: x < len(space_sample), idx))] = note.pitch

    data.append(space_sample)

    data_monophonic = {
        'vector': tuple(data)
    }

    return data_monophonic


def to_data_melody(data_midi, offset_s_audio, duration_s_audio, sample_rate=.0029):

    data = list()

    data.append(sample_rate)

    space_sample = np.zeros(int(duration_s_audio/sample_rate))

    # TODO: change these
    beats_clip = 208
    raise 'one should not hardcode things'

    def beat_to_second(beat):
        return (duration_s_audio/beats_clip) * beat

    def second_to_index(s, array):
        return int(s / duration_s_audio * len(array))

    for note in data_midi:
        offset_i_note = second_to_index(beat_to_second(note.beat_start), space_sample)
        duration_i_note = second_to_index(beat_to_second(note.beats_duration), space_sample)
        idx = list(range(offset_i_note, offset_i_note + duration_i_note))
        space_sample[idx] = librosa.midi_to_hz(note.pitch)

    data.append(space_sample)

    data_melody = {
        'vector': tuple(data)
    }

    return data_melody


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

        # TODO: move this somewhere else
        if len(chord_midi.pitches) < 4:
            chord_midi.add(music21.pitch.Pitch(chord_midi.pitches[0].midi + 12))

        events_chords[event['timestamp']] = chord_midi

    return events_chords
