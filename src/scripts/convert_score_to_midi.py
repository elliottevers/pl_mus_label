from information_retrieval import extraction as ir
from message import messenger as mes
import argparse
import librosa
from typing import List, Dict, Any
from filter import vamp as vamp_filter
from convert import vamp as vamp_convert
from preprocess import vamp as prep_vamp
from postprocess import music_xml as postp_mxl
from music import song
import music21
import json
from utils import utils


def main(args):
    messenger = mes.Messenger()

    messenger.message(['running'])

    score_export = postp_mxl.thaw_stream(
        utils.CLIPS_EXPORT
    )

    score_export.show('midi')

    messenger.message(['done'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract Chords')

    args = parser.parse_args()

    main(args)
