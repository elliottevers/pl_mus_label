import vamp
import librosa
from mido import MidiFile, MidiTrack, Message, MetaMessage
from typing import List, Dict, Any, Optional, Tuple
import music21
from music21 import interval

data, rate = librosa.load("lodi.wav")

# extract melody
# TODO: hit Flask endpoint that serves melody extraction model
file_midi = MidiFile('lodi.mid')

filename_output = 'lodi_chords.mid'

# extract harmony
ms_to_label_chord: List[Dict[float, Any]] = vamp.collect(data, rate, 'nnls-chroma:chordino')['list']

# extract segments
segments = vamp.collect(data, rate, 'qm-vamp-plugins:qm-segmenter')

# extract BPM
tempo = vamp.collect(data, rate, 'vamp-example-plugins:fixedtempo')

# synchronize?!?!?!?

bpm = 60

resolution = 1000

ms_to_pitches_chord: Dict[float, List[music21.pitch.Pitch]] = dict()

for chord in ms_to_label_chord:

    chord_label = chord['label'].replace('b', '-')  # have to use '-' for flat symbol

    try:
        chord_pitches: Tuple = music21.harmony.ChordSymbol(chord_label).pitches
    except ValueError:
        chord_pitches: Tuple = ()

    ms_to_pitches_chord[float(chord['timestamp'])] = list(chord_pitches)


# TODO: assume 4 pitches per chord, add root note to triads
# TODO: add support for arbitrary amount of pitches per chord

ms_to_pitches_chord_filtered: Dict[float, List[music21.pitch.Pitch]] = dict()

for ms, pitches in ms_to_pitches_chord.items():
    if len(pitches) == 4:
        ms_to_pitches_chord_filtered[ms] = ms_to_pitches_chord[ms]
    elif len(pitches) == 3:
        pitch_extra = pitches[0]
        # pitch_extra.transpose('P8')
        ms_to_pitches_chord[ms].append(pitch_extra.transpose('P8'))
        ms_to_pitches_chord_filtered[ms] = ms_to_pitches_chord[ms]


track_chords = MidiTrack()

track_chords.append(MetaMessage('set_tempo', tempo=1000000, time=0))

track_chords.append(Message('note_on', note=int(0), velocity=127, time=0, channel=1))
track_chords.append(Message('note_on', note=int(0), velocity=127, time=0, channel=2))
track_chords.append(Message('note_on', note=int(0), velocity=127, time=0, channel=3))
track_chords.append(Message('note_on', note=int(0), velocity=127, time=0, channel=4))

duration_ms_last_note = 0

note_channel_1_last = 0
note_channel_2_last = 0
note_channel_3_last = 0
note_channel_4_last = 0

time_ms_last = 0

for time_ms, chord in ms_to_pitches_chord_filtered.items():

    duration_ms_last_note = time_ms - time_ms_last

    note_channel_1 = chord[0].midi
    note_channel_2 = chord[1].midi
    note_channel_3 = chord[2].midi
    note_channel_4 = chord[3].midi

    off = int(duration_ms_last_note * 1000)

    track_chords.append(Message('note_off', note=int(note_channel_1_last), velocity=127, time=off, channel=1))
    track_chords.append(Message('note_off', note=int(note_channel_2_last), velocity=127, time=0, channel=2))
    track_chords.append(Message('note_off', note=int(note_channel_3_last), velocity=127, time=0, channel=3))
    track_chords.append(Message('note_off', note=int(note_channel_4_last), velocity=127, time=0, channel=4))

    track_chords.append(Message('note_on', note=int(note_channel_1), velocity=127, time=0, channel=1))
    track_chords.append(Message('note_on', note=int(note_channel_2), velocity=127, time=0, channel=2))
    track_chords.append(Message('note_on', note=int(note_channel_3), velocity=127, time=0, channel=3))
    track_chords.append(Message('note_on', note=int(note_channel_4), velocity=127, time=0, channel=4))

    time_ms_last = time_ms

    note_channel_1_last = note_channel_1
    note_channel_2_last = note_channel_2
    note_channel_3_last = note_channel_3
    note_channel_4_last = note_channel_4


track_chords.append(
    Message('note_off', note=int(0), velocity=127, time=int(duration_ms_last_note * 1000), channel=1)
)

track_chords.append(
    Message('note_off', note=int(0), velocity=127, time=int(duration_ms_last_note * 1000), channel=2)
)

track_chords.append(
    Message('note_off', note=int(0), velocity=127, time=int(duration_ms_last_note * 1000), channel=3)
)

track_chords.append(
    Message('note_off', note=int(0), velocity=127, time=int(duration_ms_last_note * 1000), channel=4)
)

# chords = chords['list']

# track_chords =

# timestamp (begin) -> segment label (represent with percussive midi data)

# scalar
# tempo_fixed =


file_midi_chords = MidiFile(ticks_per_beat=resolution)

file_midi_chords.tracks.append(track_chords)

file_midi_chords.save(filename_output)

