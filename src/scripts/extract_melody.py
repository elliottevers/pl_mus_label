from message import messenger as mes
import argparse
from utils import utils
import os
from information_retrieval import extraction as ir
from preprocess import vamp as prep_vamp
from convert import max as conv_max


def main(args):

    use_warped = utils.b_use_warped()

    data_melody = ir.extract_melody(
        os.path.join(
            utils.get_dirname_audio_warped() if use_warped else utils.get_dirname_audio(),
            utils._get_name_project_most_recent() + '.wav'
        )
    )

    df_melody = prep_vamp.melody_to_df(
        (data_melody['vector'][0], data_melody['vector'][1]),
        index_type='s'
    )

    df_melody[df_melody['melody'] < 0] = 0

    # df_melody.plot()

    # TODO: anomaly detection
    # from saxpy.hotsax import find_discords_hotsax
    # import numpy as np
    # import pandas as pd
    # import matplotlib.pyplot as plt

    # plt.show()
    # discords = find_discords_hotsax(df_melody.values.reshape(-1, ))
    # print(discords)

    conv_max.to_coll(
        df_melody.rename(columns={'melody': 'signal'}),
        conv_max.file_ts_coll
    )

    messenger = mes.Messenger()

    messenger.message(['done', 'bang'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='extract melody from raw audio')

    # parser.add_argument('--s', help='beat start')
    #
    # parser.add_argument('--e', help='beat end')

    args = parser.parse_args()

    main(args)

