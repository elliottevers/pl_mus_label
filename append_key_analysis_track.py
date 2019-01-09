# import mido
from music21 import converter, analysis
from mido import Message, MetaMessage, MidiFile, MidiTrack, bpm2tempo
from subprocess import call as call_shell


filename_in = '/Users/elliottevers/Downloads/kitty_honky_chords_doubled.mid' # '/Users/elliottevers/Downloads/ella_dream_chords_doubled.mid'

filename_out = '/Users/elliottevers/Downloads/kitty_honky_chords_and_key_centers.mid'

filename_chords_original = '/Users/elliottevers/Downloads/Chordify_It-Wasn-t-God-Who-Made-Honky-Tonk-Angels-Kitty-Wells_Quantized_at_136_BPM.mid'

TRACK_CHORDS = 1

file = MidiFile(filename_chords_original)

track_chords = file.tracks[TRACK_CHORDS]

ppq = file.ticks_per_beat

bpm_file = 136

window_size = 256

stream = converter.parse(filename_in)

# solutions = midi_analysis.key_center_windowed_complete(
#     part=stream,
#     window_size_measures=64,
#     melody=True
# )

analyzer = analysis.discrete.BellmanBudge()

wa = analysis.windowed.WindowedAnalysis(stream.parts[0], analyzer)

solutions, color = wa.analyze(
    window_size,  # 64,
    'overlap'
)

# (len(solutions) + 64 - 1)/2

num_measures = (len(solutions) + window_size - 1)/2

notes = []

solutions = [tuple_pitch[0].midi for tuple_pitch in solutions]

for i_measure in range(1, int(num_measures)):
    notes.append(solutions[i_measure])

# generate midi track of tones

# figure out how many ticks to make each note - ppq of track to "overdub"

# listen to track together for validation

file_overdubbed = MidiFile(ticks_per_beat=ppq)

track_main = track_chords

track_overdub = MidiTrack()

track_overdub.append(
    MetaMessage(
        'time_signature',
        time=0
    )
)

track_overdub.append(
    MetaMessage(
        'set_tempo',
        tempo=bpm2tempo(bpm_file),
        time=0
    )
)

velocity = 90

for pitch_midi in solutions:
    track_overdub.append(
        Message(
            'note_on',
            note=pitch_midi,
            velocity=velocity,
            time=0
        )
    )
    track_overdub.append(
        Message(
            'note_off',
            note=pitch_midi,
            velocity=0,
            time=ppq
        )
    )

file_overdubbed.tracks.append(track_main)

file_overdubbed.tracks.append(track_overdub)

file_overdubbed.save(filename_out)

call_shell(['open', '-a', '/Applications/MidiYodi 2018.1.app/', filename_out])