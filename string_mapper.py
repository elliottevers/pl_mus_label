MAJOR = 'major'

# MIDI notes
open_string6 = 40
open_string5 = 45
open_string4 = 50
open_string3 = 55
open_string2 = 59
open_string1 = 64

num_frets = 12

range_full_guitar = list(range(open_string6, open_string1 + num_frets))

string6 = list(range(open_string6, open_string6 + num_frets))
string5 = list(range(open_string5, open_string5 + num_frets))
string4 = list(range(open_string4, open_string4 + num_frets))
string3 = list(range(open_string3, open_string3 + num_frets))
string2 = list(range(open_string2, open_string2 + num_frets))
string1 = list(range(open_string1, open_string1 + num_frets))

scale = MAJOR

trichord_order_major = [0, 2, 2], [0, 2, 2], [0, 1, 2], [0, 1, 2], [0, 2, 1], [0, 2, 1], [0, 2, 2]

root = 3  # fret number on string 6
frets_per_string_const = 3
fingering = dict()

note_midi_root = range_full_guitar[0] + root

notes_scale = set()

intervals_major = [0, 2, 2, 1, 2, 2, 2, 1]

intervals_major_octave = []
acc = 0

for interval in intervals_major:
    intervals_major_octave.append(acc)
    acc += interval

intervals_major_octave.append(12)

# up

note_current = note_midi_root

notes_scale.add(note_current)

while note_current <= range_full_guitar[-1]:
    for interval in intervals_major:
        note_current += interval
        if note_current <= range_full_guitar[-1]:
            notes_scale.add(note_current)


# down

note_current = note_midi_root

notes_scale.add(note_current)

while note_current >= range_full_guitar[0]:
    for interval in reversed(intervals_major):
        note_current -= interval
        if note_current >= range_full_guitar[0]:
            notes_scale.add(note_current)

PERFECT_FOURTH = 5

interval_skip = PERFECT_FOURTH

notes_pivot = []

strings = [string6, string5, string4, string3, string2, string1]


for i, _ in enumerate(strings):
    notes_pivot.append(note_midi_root + i * interval_skip)

for i, note in enumerate(reversed(notes_pivot)):
    for j in range(0, interval_skip):
        fingering[note + j] = {'string': i + 1}


for note in range_full_guitar:
    if note < note_midi_root:
        fingering[note] = {'string': 6, 'fret': string6.index(note)}
    if note > notes_pivot[-1] + interval_skip:
        fingering[note] = {'string': 1, 'fret': string1.index(note)}

for note, placement in fingering.items():
    if 'fret' not in placement:
        placement['fret'] = strings[6 - placement['string']].index(note)



