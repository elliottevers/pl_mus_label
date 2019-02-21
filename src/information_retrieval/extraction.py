# import jsonpickle
import librosa
import vamp
import pickle
import os
from utils import utils


files_stub = {
    'melody': 'test/stubs_pickle/python/melody_tswift_teardrops.json',
    'segments': 'test/stubs_pickle/python/segments_tswift_teardrops.json',
    'chords': 'test/stubs_pickle/python/chords_tswift_teardrops.json',
    'tempo': 'test/stubs_pickle/python/tempo_tswift_teardrops.json',
    'beats': 'test/stubs_pickle/python/beats_tswift_teardrops.json'
}


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
    stub=False
):
    if stub:
        with open(files_stub['segments'], 'r') as file:
            data_segments = jsonpickle.decode(file.read())

        return data_segments
    else:
        raise 'did you actually think this was real?'


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


def _is_cached():
    raise 'not implemented'


def _get_cached_wav():
    raise 'not implemented'


def extract_tempo(
    filename_wav,
    # stub=False
):
    # if stub:
    #     with open(files_stub['tempo'], 'r') as file:
    #         data_tempo = jsonpickle.decode(file.read())
    #
    #     return data_tempo
    # else:
    #     raise 'did you actually think this was real?'

    if _is_cached(filename_wav):
        with open(_get_cached_wav(filename_wav), 'r') as file:
            data_tempo = pickle.decode(file.read())

        return data_tempo
    else:
        data, rate = librosa.load(os.path.join(_get_dirname_audio(), filename_wav))

        data_tempo = vamp.collect(data, rate, "vamp-aubio:aubiotempo")

        utils.to_pickle(
            data_tempo,
            _get_cached_wav(
                filename_wav
            )
        )

    return data_tempo


def extract_beats(
    filename_wav,
    from_cache=False
):
    if from_cache and _is_cached(filename_wav):
        with open(_get_cached_wav(filename_wav), 'r') as file:
            data_beats = pickle.decode(file.read())

        return data_beats
    else:
        data, rate = librosa.load(os.path.join(_get_dirname_audio(), filename_wav))

        data_beats = vamp.collect(data, rate, "qm-vamp-plugins:qm-barbeattracker")

        utils.to_pickle(
            data_beats,
            _get_cached_wav(
                filename_wav
            )
        )

    return data_beats
