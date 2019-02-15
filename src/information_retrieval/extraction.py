import jsonpickle

files_stub = {
    'melody': 'test/stubs_pickle/python/melody_tswift_teardrops.json',
    'segments': 'test/stubs_pickle/python/segments_tswift_teardrops.json',
    'chords': 'test/stubs_pickle/python/chords_tswift_teardrops.json',
    'tempo': 'test/stubs_pickle/python/tempo_tswift_teardrops.json',
    'beats': 'test/stubs_pickle/python/beats_tswift_teardrops.json'
}


def extract_melody(
    filename_wav,
    stub=False
):
    if stub:
        with open(files_stub['melody'], 'r') as file:
            data_melody = jsonpickle.decode(file.read())

        return data_melody
    else:
        raise 'did you actually think this was real?'


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
    stub=False
):
    if stub:
        with open(files_stub['chords'], 'r') as file:
            data_chords = jsonpickle.decode(file.read())

        return data_chords
    else:
        raise 'did you actually think this was real?'


def extract_tempo(
    filename_wav,
    stub=False
):
    if stub:
        with open(files_stub['tempo'], 'r') as file:
            data_tempo = jsonpickle.decode(file.read())

        return data_tempo
    else:
        raise 'did you actually think this was real?'


def extract_beats(
    filename_wav,
    stub=False
):
    if stub:
        with open(files_stub['beats'], 'r') as file:
            data_beats = jsonpickle.decode(file.read())

        return data_beats
    else:
        raise 'did you actually think this was real?'
