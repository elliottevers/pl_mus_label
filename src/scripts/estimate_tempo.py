from information_retrieval import extraction as ir
import argparse


def main(args):
    tempo_estimate = ir.extract_tempo(
        # args.name_project
    )

    print(tempo_estimate)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Estimate Tempo')

    # parser.add_argument('name_project', help='audio file from which to extract tempo')

    args = parser.parse_args()

    main(args)
