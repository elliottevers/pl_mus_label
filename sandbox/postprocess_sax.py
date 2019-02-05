import music21
import numpy as np
from scipy import signal

# make command line argument
kernel_size = 199

filtered = True

interval_transposition = 'm2'

# dirname = '/Users/elliottevers/Documents/git-repos.nosync/music'
dirname = '/Users/elliottevers/Documents/Documents - Elliott’s MacBook Pro/git-repos.nosync/music/'

filename_txt = 'test.txt'

filepath_read = dirname + '/' + filename_txt

filepath_write = dirname + '/' + 'sandbox/write_sax.txt'

alphabet_map = {
    'a': 'C3',
    'b': 'D-3',
    'c': 'D3',
    'd': 'E-3',
    'e': 'E3',
    'f': 'F3',
    'g': 'G-3',
    'h': 'G3',
    'i': 'A-3',
    'j': 'A3',
    'k': 'A#3',
    'l': 'B3',
    'm': 'C4',
    'n': 'C#4',
    'o': 'D4',
    'p': 'D#4',
    'q': 'E4',
    'r': 'F4',
    's': 'F#4',
    't': 'G4',
    'u': 'G#4',
    'v': 'A4',
    'w': 'A#4',
    'x': 'B4',
    'y': 'C5',
    'z': 'C#5'
}

content = []

if not filtered:
    with open(filepath_read, 'r') as f:
        for line in f:
            letter = line.rstrip()
            if letter == 'i':
                content.append(str(0))
            elif letter == 'h':
                content.append(str(0))
            else:
                content.append(str(music21.pitch.Pitch(alphabet_map[letter]).frequency))

    with open(filepath_write, 'w') as f:
        for i_line, line in enumerate(content):
            f.write(str(i_line + 1) + ',' + ' ' + line + ';' + '\n')
else:
    with open(filepath_read, 'r') as f:
        for line in f:
            letter = line.rstrip()
            if letter == 'i':
                content.append(0)
            elif letter == 'h':
                content.append(0)
            else:
                content.append(music21.pitch.Pitch(alphabet_map[letter]).transpose(interval_transposition).frequency)

    filtered = signal.medfilt(np.array(content, dtype=np.float), kernel_size=kernel_size)

    filtered_list = filtered.tolist()

    with open(filepath_write, 'w') as f:
        for i_line, line in enumerate(filtered_list):
            f.write(str(i_line + 1) + ',' + ' ' + str(line) + ';' + '\n')

