import vamp, librosa, os, json, pandas as pd, numpy as np

prefix_metadata = 'meta_'

filename_wav = 'tswift_teardrops.wav'

dirname_audio = '/Users/elliottevers/Documents/DocumentsSymlinked/git-repos.nosync/audio/youtube/'

dirname_melody_out = '/Users/elliottevers/Documents/DocumentsSymlinked/git-repos.nosync/music/src/information_retrieval/out/hz_raw/'

filename_csv_melody_out = ''.join([filename_wav.split('.')[0], '.csv'])

filename_json_metadata_out = ''.join([prefix_metadata, filename_wav.split('.')[0], '.json'])

dirname_audio = os.path.dirname(dirname_audio)

dirname_melody_out = os.path.dirname(dirname_melody_out)

data, rate = librosa.load(os.path.join(dirname_audio, filename_wav))

melody = vamp.collect(data, rate, "mtg-melodia:melodia")

metadata = {
    'sample_rate': melody['vector'][0].to_float(),
    'length_samples': len(melody['vector'][1]),
    'length_ms': melody['vector'][0].to_float() * len(melody['vector'][1])
}

df = pd.DataFrame(
    melody['vector'][1],
    columns=['sample']
)

df['ms'] = pd.DataFrame(
    np.full(
        (len(melody['vector'][1]), ),
        melody['vector'][0].to_float(),
        np.float32
    )
).cumsum()

df = df[['ms', 'sample']]

with open(os.path.join(dirname_melody_out, filename_json_metadata_out), 'w') as fp:
    json.dump(metadata, fp)

df.to_csv(os.path.join(dirname_melody_out, filename_csv_melody_out), header=False, index=False)

