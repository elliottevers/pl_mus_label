import numpy as np
import collections
import librosa
from mido import Message, MidiFile, MidiTrack, MetaMessage

ms_to_pitch = collections.OrderedDict()
with open('/Users/elliottevers/Documents/git-repos.nosync/audio_to_midi_melodia/train01.txt', 'r') as file_local:
    for line in file_local:
        ms_to_pitch[float(line.split()[0])] = int(float(line.split()[1]))

bpm = 60

resolution = 1000

mid = MidiFile(ticks_per_beat=resolution)

ms_to_pitch_filtered = collections.OrderedDict()

pitch_last = 0

for time_ms, pitch_hertz in ms_to_pitch.iteritems():

    if pitch_hertz != pitch_last:
        ms_to_pitch_filtered[time_ms] = pitch_hertz

    pitch_last = pitch_hertz


track = MidiTrack()

mid.tracks.append(track)

track.append(MetaMessage('set_tempo', tempo=1000000, time=0))

track.append(Message('note_on', note=0, velocity=127, time=0))

duration_ms_last_note = 0

note_midi_last_note = 0

time_ms_last = 0

for time_ms, pitch_hertz in ms_to_pitch_filtered.iteritems():

    if pitch_hertz == 0:
        note_midi = 0
    else:
        note_midi = librosa.hz_to_midi(pitch_hertz)[0]

    duration_ms_last_note = time_ms - time_ms_last

    track.append(Message('note_off', note=int(note_midi_last_note), velocity=127, time=int(duration_ms_last_note * 1000)))

    track.append(Message('note_on', note=int(note_midi), velocity=127, time=0))

    time_ms_last = time_ms

    note_midi_last_note = note_midi


track.append(Message('note_off', note=0, velocity=127, time=0))


mid.save('train01.mid')