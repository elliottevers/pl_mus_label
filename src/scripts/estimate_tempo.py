from information_retrieval import extraction as ir
from filter import seconds as s_filt
from preprocess import vamp as prep_vamp
from message import messenger as mes
import argparse


def main(args):
    messenger = mes.Messenger()

    messenger.message(['running'])

    filename_wav = args.filename

    data_tempo = ir.extract_tempo(
        filename_wav
    )

    tempomap = prep_vamp.extract_tempomap(
        data_tempo
    )

    # TODO: implement that median filter
    fixed_tempo_estimate = s_filt.get_fixed_tempo_estimate(
        tempomap
    )

    messenger.message(fixed_tempo_estimate)

    messenger.message(['done'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Estimate Tempo')

    parser.add_argument('filepath', help='audio file from which to extract tempo')

    args = parser.parse_args()

    main(args)
