from message import messenger as mes
import argparse
from utils import utils
import os
import subprocess


def main(args):

    utils.write_name_project(args.name_project)

    utils.create_dir_project()

    utils.create_dir_audio()

    utils.create_dir_audio_warped()

    utils.create_dir_session()

    dir_downloads = os.path.join(
        utils.dir_projects,
        'downloads'
    )

    command_to_downloads = [
        args.path_executable,
        '-x' if args.x else '',
        '--o',
        dir_downloads + '/' + args.name_project + '.%(ext)s',
        '--audio-format',
        args.audio_format,
        '--ffmpeg-location',
        args.ffmpeg_location,
        args.url[0]
    ]

    subprocess.run(
        command_to_downloads,
        stdout=subprocess.PIPE
    ).stdout.rstrip().decode("utf-8")

    dir_audio = utils.get_path_dir_audio()

    command_to_audio = [
        args.path_executable,
        '-x' if args.x else '',
        '--o',
        dir_audio + '/' + args.name_project + '.%(ext)s',
        '--audio-format',
        args.audio_format,
        '--ffmpeg-location',
        args.ffmpeg_location,
        args.url[0]
    ]

    subprocess.run(
        command_to_audio,
        stdout=subprocess.PIPE
    ).stdout.rstrip().decode("utf-8")

    messenger = mes.Messenger(key_route='')

    messenger.message(['done'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Given YouTube URL download audio')

    parser.add_argument('--name-project', help='name of project')

    parser.add_argument('--path-executable', help='path to YouTube DL')

    parser.add_argument('-x', help='audio only', action='store_true')

    # parser.add_argument('--o', help='output dir')

    parser.add_argument('--audio-format', help='e.g, wav')

    parser.add_argument('--ffmpeg-location', help='path to ffmpeg')

    parser.add_argument('url', help='YouTube URL', nargs=1)

    args = parser.parse_args()

    main(args)
