# from information_retrieval import extraction as ir
# from message import messenger as mes
# import argparse
# from preprocess import vamp as prep_vamp
# from utils import utils
# from convert import max as conv_max
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
#     filename_wav = args.filename
#
#     data_melody = ir.extract_melody(
#         filename_wav
#     )
#
#     df_melody = prep_vamp.melody_to_df(
#         data_melody,
#         index_type='s'
#     )
#
#     conv_max.to_coll(
#         df_melody,
#         filepath=utils.FILE_COLL_MELODY_RAW
#     )
#
#     messenger.message(
#         [
#             utils.MESSAGE_FILE_COLL,
#             utils.FILE_COLL_MELODY_RAW
#         ]
#     )
#
#     messenger.message(['done'])
#
#
# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='Extract Melody')
#
#     parser.add_argument('filepath', help='audio file from which to extract melody')
#
#     args = parser.parse_args()
#
#     main(args)
