from information_retrieval import extraction as ir
# from message import messenger as mes
import argparse
import numpy as np
import librosa
from information_retrieval import extraction
import os


def main(args):
    # messenger = mes.Messenger()
    #
    # messenger.message(['running'])

    # filename_wav = args.filename

    beat_start = args.s

    beat_end = args.e

    filename_wav = os.path.join(
        extraction._get_dirname_audio_warped(),
        extraction._get_name_project_most_recent() + '.wav'
    )

    y, sr = librosa.load(
        filename_wav
    )

    duration_s_audio = librosa.get_duration(
        y=y,
        sr=sr
    )

    if args.m:
        beatmap_manual = np.linspace(
            0,
            float(duration_s_audio),
            int(beat_end) - int(beat_start) + 1
        )
    else:
        return

    beatmap_estimated = ir.extract_beats(
        filename_wav
    )

    beatmap_manual.tolist()

    exit(0)
    # messenger.message(['done'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Estimate Beats')

    # parser.add_argument('filepath', help='audio file from which to extract beat estimates')

    parser.add_argument('--s', help='beat start')

    parser.add_argument('--e', help='beat end')

    parser.add_argument('-m', help='manual', action='store_true')

    args = parser.parse_args()

    main(args)
