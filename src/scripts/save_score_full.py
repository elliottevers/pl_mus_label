# from message import messenger as mes
# import argparse
# from utils import utils
# import os
# from utils import musix_xml as utils_mxl
# import music21
#
#
# def main(args):
#
#     messenger = mes.Messenger()
#
#     score_full = music21.stream.Score()
#
#     for name_part in ['melody', 'chord', 'bass', 'key_center', 'segment']:
#         filename_part = os.path.join(
#             utils.get_dirname_score(),
#             name_part,
#             utils._get_name_project_most_recent() + '.pkl'
#         )
#         if os.path.isfile(filename_part):
#             stream_part = utils_mxl.thaw_stream(
#                 filename_part
#             )
#             score_full.append(stream_part)
#
#     score_full.show()
#
#     messenger.message(['done'])
#
#
# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='Extract Segments')
#
#     args = parser.parse_args()
#
#     main(args)
