from information_retrieval import extraction as ir
from message import messenger as mes
import argparse
import librosa
from typing import List, Dict, Any
from filter import vamp as vamp_filter
from convert import vamp as vamp_convert
from preprocess import vamp as prep_vamp
from postprocess import music_xml as postp_mxl, midi as postp_mid
from music import song
import music21
import json
from utils import utils


# s = music21.stream.Stream()
# n = music21.note.Note('g#')
# n.quarterLength = .5
# s.repeatAppend(n, 4)
# mf = music21.midi.translate.streamToMidiFile(s)
#
# for event in mf.tracks[0].events:
#     event.channel = 2
#
# mf.open('/Users/elliottevers/Downloads/midi_test.mid', 'wb')
#
# mf.write()
#
# mf.close()

# with open('/Users/elliottevers/Downloads/midi_test.mid', 'w') as outfile:
#     mf.write()

# len(mf.tracks)
#
# len(mf.tracks[0].events)

# exit(0)

def main(args):
    messenger = mes.Messenger()

    messenger.message(['running'])

    score_export = postp_mxl.thaw_stream(
        utils.CLIPS_EXPORT
    )

    postp_mid.to_mid(
        score_export,
        fp=utils.CLIPS_EXPORT_MID
    )

    # score_export.write(
    #     'midi',
    #     fp=utils.CLIPS_EXPORT_MID
    # )

    messenger.message(['done'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract Chords')

    args = parser.parse_args()

    main(args)
