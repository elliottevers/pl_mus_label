# from information_retrieval import extraction as ir
# from message import messenger as mes
# import argparse
# import librosa
# from typing import List, Dict, Any
# from filter import vamp as vamp_filter
# from convert import vamp as vamp_convert
# from preprocess import vamp as prep_vamp
# from postprocess import music_xml as postp_mxl
# from music import song
# import music21
# import json
# from utils import utils
# from postprocess import live as postp_live
#
#
# # TODO: get the filepath of the cache module
# filename_chords_to_live = utils.get_path_cache(utils.CHORD_LIVE)
#
#
# def main(args):
#     messenger = mes.Messenger()
#
#     messenger.message(['running'])
#
#     score_chords = postp_mxl.thaw_stream(
#         utils.FILE_CHORD_SCORE
#     )
#
#     # SCORE UPPER VOICES
#
#     # TODO: postp_mxl should be agnostic to dataframes
#     score_upper_voicings = postp_mxl.extract_upper_voices(
#         score_chords
#     )
#
#     # TODO: postp_mxl should be agnostic to dataframes
#     dict_write_json_live_upper_voicings = postp_mxl.to_json_live(
#         score_upper_voicings,
#         parts=['bass']
#     )
#
#     # SCORE BASS
#
#     score_bass = postp_mxl.extract_bass(
#         score_chords
#     )
#
#     dict_write_json_live_bass = postp_mxl.to_json_live(
#         score_bass,
#         parts=['bass']
#     )
#
#     # WRITE BOTH
#
#     postp_mxl.freeze_stream(
#         stream=score_upper_voicings,
#         filepath=utils.FILE_UPPER_VOICINGS_SCORE
#     )
#
#     postp_mxl.freeze_stream(
#         stream=score_bass,
#         filepath=utils.FILE_BASS_SCORE
#     )
#
#     utils.to_json_live(
#         dict_write_json_live_upper_voicings,
#         filename_chords_to_live=utils.FILE_UPPER_VOICINGS_LIVE
#     )
#
#     utils.to_json_live(
#         dict_write_json_live_bass,
#         filename_chords_to_live=utils.FILE_BASS_LIVE
#     )
#
#     messenger.message(['done'])
#
#
# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='Extract bass from chords and render to Ableton track')
#
#     parser.add_argument('filepath', help='audio file from which to extract chords')
#
#     args = parser.parse_args()
#
#     main(args)
