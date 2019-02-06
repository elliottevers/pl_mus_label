import music21
import numpy as np
from scipy import signal
import pandas as pd
import os
import typing
import matplotlib.pyplot as plt

dirname_repo = os.path.dirname('/Users/elliottevers/Documents/Documents - Elliott’s MacBook Pro/git-repos.nosync/music/')

dirname_melody = os.path.join(dirname_repo, 'information_retrieval/output/')

filename_melody = 'melody_tswift_teardrops.txt'

dirname_out_multi_ts = os.path.join(
    dirname_repo, 'filter/out/hz_filtered/'
)

filter = 'medfilt'

params = {
    'kernel_size': [
        111,
        311,
        511
    ]
}

coll_txt_melody = os.path.join(
    dirname_repo, 'postprocess/out/hz_raw/melody_tswift_teardrops.txt'
)

# csv_extracted_melody = '/Users/elliottevers/Documents/Documents - Elliott’s MacBook Pro/git-repos.nosync/music/information_retrieval/output/melody_tswift_teardrops.csv'

# coll flat file -> multiple coll flat files, based on filtering params
# coll file -> numpy array -> pandas series -> (can we call scipy on series, can we have multiple ts?)
# -> muliple coll files

melody_df = pd.read_csv(
    coll_txt_melody,
    header=None,
    names=['ms_sample', 'hz_signal']
)

# get rid of semi-colons at end
melody_df['hz_signal'] = melody_df['hz_signal'].map(lambda line: line.rstrip(';')).astype(np.float)

melody_ts_master: pd.Series = melody_df.loc[:, 'hz_signal']

for name_argument, values in params.items():
    for i_value, value in enumerate(values):
        melody_df['filtered' + str(i_value)] = \
            pd.Series(
                getattr(signal, filter)(melody_ts_master.as_matrix().reshape(-1, ), **{name_argument: value}),
                dtype=np.float
            )

melody_df[melody_df.columns[-1]] = melody_df[melody_df.columns[-1]].astype(str).map(lambda entry: entry + ';')

melody_df.to_csv(
    os.path.join(
        dirname_repo,
        'filter/out/hz_filtered/melody_tswift_teardrops.txt'
    ),
    header=None
)

# plotting
# melody_df['hz_signal'].plot()
# melody_df['filtered2'].plot()
# plt.show()

# exit(0)

exit(0)

# make command line argument
kernel_size = 199

filtered = True

interval_transposition = 'm2'

dirname = '/Users/elliottevers/Documents/git-repos.nosync/music'

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
