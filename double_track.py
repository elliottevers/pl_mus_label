import mido
import filter.midi as midi_filter
from subprocess import call as call_shell

filename_in = '/Users/elliottevers/Downloads/Chordify_It-Wasn-t-God-Who-Made-Honky-Tonk-Angels-Kitty-Wells_Quantized_at_136_BPM.mid'

filename_out = '/Users/elliottevers/Downloads/kitty_honky_chords_doubled.mid'

TRACK_CHORDS = 1  # 1

TRACK_BASS = 2  # 2

bpm_file = 136  # 75

file = mido.MidiFile(filename_in)

ppq = file.ticks_per_beat

track_chords = file.tracks[TRACK_CHORDS]

track_doubled = midi_filter.pad(
    track_chords,
    bpm_file,
    2
)

file_out = mido.MidiFile(ticks_per_beat=ppq)

file_out.tracks.append(track_doubled)

file_out.save(filename_out)

call_shell(['open', '-a', '/Applications/MidiYodi 2018.1.app/', filename_out])