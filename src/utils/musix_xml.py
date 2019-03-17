import music21


def freeze_stream(stream, filepath) -> None:
    stream_frozen = music21.freezeThaw.StreamFreezer(stream)
    stream_frozen.write(fmt='pickle', fp=filepath)


def thaw_stream(filepath) -> music21.stream.Stream:
    thawer = music21.freezeThaw.StreamThawer()
    thawer.open(fp=filepath)
    return thawer.stream
