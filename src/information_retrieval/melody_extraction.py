import vamp, librosa, os

prefix_melody = 'melody_'

filename_wav = 'tswift_teardrops.wav'

filename_csv_melody_out = ''.join([prefix_melody, filename_wav.split('.')[0], '.csv'])

dirname_audio = os.path.dirname('/Users/elliottevers/Documents/Documents - Elliott’s MacBook Pro/git-repos.nosync/audio/youtube/')

dirname_melody_out = os.path.dirname('/Users/elliottevers/Documents/Documents - Elliott’s MacBook Pro/git-repos.nosync/music/information_retrieval/output/')

data, rate = librosa.load(os.path.join(dirname_audio, filename_wav))

melody = vamp.collect(data, rate, "mtg-melodia:melodia")

with open(os.path.join(dirname_melody_out, filename_csv_melody_out), 'w') as f:
    sample_rate = melody['vector'][0]
    sum_sample_time = sample_rate  # initialize
    for sample_hz in melody['vector'][1]:
        line = str(sum_sample_time) + ',' + str(sample_hz) + '\n'
        f.write(line.lstrip())
        sum_sample_time += sample_rate
