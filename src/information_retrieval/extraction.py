import librosa
import vamp
import os
from preprocess import vamp as vamp_prep
from typing import List, Dict, Any, Optional, Tuple
import subprocess
from utils import utils

dir_projects = os.path.dirname('/Users/elliottevers/Documents/git-repos.nosync/tk_music_projects/')
file_log = os.path.join(dir_projects, '.log.txt')


def extract_melody(
    filename_wav
):
    data, rate = librosa.load(os.path.join(utils.get_dirname_audio_warped(), filename_wav))

    data_melody = vamp.collect(data, rate, "mtg-melodia:melodia")

    return data_melody


def extract_segments(
    filename_wav
):
    data, rate = librosa.load(
        filename_wav
    )

    data_segments = vamp.collect(data, rate, 'qm-vamp-plugins:qm-segmenter')

    return data_segments['list']


def extract_tempo():
    project_name = utils._get_name_project_most_recent()

    data, rate = librosa.load(
        os.path.join(utils.get_dirname_audio(), project_name + '.wav')
    )

    data_tempo = vamp.collect(data, rate, "qm-vamp-plugins:qm-tempotracker")

    subprocess.run(
        ['mkdir', os.path.join(utils.get_project_dir(), 'tempo')],
        stdout=subprocess.PIPE
    )

    estimate_tempo = vamp_prep.to_tempo(data_tempo)

    utils.to_pickle(
        estimate_tempo,
        os.path.join(utils.get_dirname_audio(), project_name)
    )

    return estimate_tempo


def extract_beats(
    filename_wav
):
    data, rate = librosa.load(
        filename_wav
    )

    data_beats = vamp.collect(data, rate, "qm-vamp-plugins:qm-tempotracker")

    return vamp_prep.extract_beatmap(data_beats)


def extract_chords(
    filename_wav
):
    data, rate = librosa.load(
        filename_wav
    )

    data_chords = vamp.collect(data, rate, "nnls-chroma:chordino")

    s_to_label_chords: List[Dict[float, Any]] = [
        {'timestamp': obj['timestamp'].to_float(), 'label': obj['label']} for obj in data_chords['list']
    ]

    return s_to_label_chords
