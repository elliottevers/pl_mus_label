# import jsonpickle
import librosa
import vamp
import pickle
import os
from utils import utils
from preprocess import vamp as vamp_prep

import subprocess

dir_projects = os.path.dirname('/Users/elliottevers/Documents/DocumentsSymlinked/git-repos.nosync/tk_music_projects/')
file_log = os.path.join(dir_projects, '.log.txt')


# files_stub = {
#     'melody': 'test/stubs_pickle/python/melody_tswift_teardrops.json',
#     'segments': 'test/stubs_pickle/python/segments_tswift_teardrops.json',
#     'chords': 'test/stubs_pickle/python/chords_tswift_teardrops.json',
#     'tempo': 'test/stubs_pickle/python/tempo_tswift_teardrops.json',
#     'beats': 'test/stubs_pickle/python/beats_tswift_teardrops.json'
# }


def extract_melody(
    filename_wav,
    from_cache=False
):
    if _is_cached(filename_wav):
        with open(_get_cached_wav(filename_wav), 'r') as file:
            data_melody = pickle.decode(file.read())

        return data_melody
    else:
        data, rate = librosa.load(os.path.join(_get_dirname_audio(), filename_wav))

        data_melody = vamp.collect(data, rate, "mtg-melodia:melodia")

        utils.to_pickle(
            data_melody,
            _get_cached_wav(
                filename_wav
            )
        )

    return data_melody


def extract_segments(
    filename_wav,
    from_cache=False
):
    if from_cache and _is_cached(filename_wav):
        with open(_get_cached_wav(filename_wav), 'r') as file:
            data_segments = pickle.decode(file.read())

        return data_segments
    else:
        data, rate = librosa.load(os.path.join(_get_dirname_audio(), filename_wav))

        data_segments = vamp.collect(data, rate, 'qm-vamp-plugins:qm-segmenter')
        # data_segments = vamp.collect(data, rate, 'nnls-chroma:segmentino')

        utils.to_pickle(
            data_segments,
            _get_cached_wav(
                filename_wav
            )
        )

    return data_segments


def extract_chords(
    filename_wav,
    from_cache=False
):
    if from_cache and _is_cached(filename_wav):
        with open(_get_cached_wav(filename_wav), 'r') as file:
            data_chords = pickle.decode(file.read())

        return data_chords
    else:
        data, rate = librosa.load(os.path.join(_get_dirname_audio(), filename_wav))

        data_chords = vamp.collect(data, rate, "nnls-chroma:chordino")

        utils.to_pickle(
            data_chords,
            _get_cached_wav(
                filename_wav
            )
        )

    return data_chords


def _is_cached(filename):
    return False


def _get_cached_wav():
    raise 'not implemented'


def _get_name_project_most_recent():
    return subprocess.run(
        ['head', '-1', file_log],
        stdout=subprocess.PIPE
    ).stdout.rstrip().decode("utf-8")


def _get_project_dir():
    return os.path.join(dir_projects, 'projects', _get_name_project_most_recent())


def _get_dirname_audio():
    return os.path.join(_get_project_dir(), 'audio')


def _get_dirname_audio_warped():
    return os.path.join(_get_project_dir(), 'audio_warped')


def _get_dirname_tempo():
    return os.path.join(_get_project_dir(), 'tempo')


# def _get_wav_raw():
#     return os.path.join(_get_dirname_audio(), _get_name_project_most_recent() + '.wav')


def extract_tempo(

):

    # if _is_cached(project_name):
    #     with open(_get_cached_wav(project_name), 'r') as file:
    #         data_tempo = pickle.decode(file.read())
    #
    #     return data_tempo
    # else:

    project_name = _get_name_project_most_recent()

    data, rate = librosa.load(
        os.path.join(_get_dirname_audio(), project_name + '.wav')
    )

    data_tempo = vamp.collect(data, rate, "qm-vamp-plugins:qm-tempotracker")

    results = subprocess.run(
        ['mkdir', os.path.join(_get_project_dir(), 'tempo')],
        stdout=subprocess.PIPE
    )

    estimate_tempo = vamp_prep.to_tempo(data_tempo)

    utils.to_pickle(
        estimate_tempo,
        os.path.join(_get_dirname_audio(), project_name)
    )

    return estimate_tempo


def extract_beats(
    filename_wav,
    # from_cache=False
):
    # if from_cache and _is_cached(filename_wav):
    #     with open(_get_cached_wav(filename_wav), 'r') as file:
    #         data_beats = pickle.decode(file.read())
    #
    #     return data_beats
    # else:
    #     data, rate = librosa.load(os.path.join(_get_dirname_audio(), filename_wav))
    #
    #     data_beats = vamp.collect(data, rate, "qm-vamp-plugins:qm-barbeattracker")
    #
    #     utils.to_pickle(
    #         data_beats,
    #         _get_cached_wav(
    #             filename_wav
    #         )
    #     )
    #
    # return data_beats






    # project_name = _get_name_project_most_recent()
    #
    # data, rate = librosa.load(
    #     os.path.join(_get_dirname_audio(), project_name + '.wav')
    # )
    #
    # data_tempo = vamp.collect(data, rate, "qm-vamp-plugins:qm-tempotracker")
    #
    # results = subprocess.run(
    #     ['mkdir', os.path.join(_get_project_dir(), 'tempo')],
    #     stdout=subprocess.PIPE
    # )
    #
    # estimate_tempo = vamp_prep.to_tempo(data_tempo)
    #
    # utils.to_pickle(
    #     estimate_tempo,
    #     os.path.join(_get_dirname_audio(), project_name)
    # )

    data, rate = librosa.load(
        filename_wav
    )

    data_beats = vamp.collect(data, rate, "qm-vamp-plugins:qm-tempotracker")

    return vamp_prep.extract_beatmap(data_beats)
