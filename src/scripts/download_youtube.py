import sys
sys.path.insert(0, '/Users/elliottevers/Documents/git-repos.nosync/tk_music_py/src')
import argparse
import subprocess
from message import messenger as mes
from utils import utils


# import pydevd
# pydevd.settrace('localhost', port=8008, stdoutToServer=True, stderrToServer=True)


def main(args):

    utils.write_name_project(args.name_project)

    utils.create_dir_project()

    utils.create_dir_audio()

    utils.create_dir_audio_warped()

    utils.create_dir_vocals()

    utils.create_dir_session()

    audio_only = args.x

    include_video = not audio_only

    if include_video:
        utils.create_dir_video()

        utils.create_dir_video_warped()

        dir_video = utils.get_path_dir_video()

        command_to_video = [
            args.path_executable,
            '--o',
            dir_video + '/' + args.name_project + '.%(ext)s',
            '-f',
            'mp4',
            '--ffmpeg-location',
            args.ffmpeg_location,
            args.url[0]
        ]

        subprocess.run(
            command_to_video,
            stdout=subprocess.PIPE
        ).stdout.rstrip().decode("utf-8")

    dir_audio = utils.get_path_dir_audio()

    command_to_audio = [
        args.path_executable,
        '-x',
        '--o',
        dir_audio + '/' + args.name_project + '.%(ext)s',
        '--audio-format',
        args.audio_format,
        '--ffmpeg-location',
        args.ffmpeg_location,
        args.url[0]
    ]

    res = subprocess.run(
        command_to_audio,
        stdout=subprocess.PIPE
    ).stdout.rstrip().decode("utf-8")

    messenger = mes.Messenger()

    messenger.message(['done', 'bang'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Given YouTube URL download audio')

    parser.add_argument('--name-project', help='name of project')

    parser.add_argument('--path-executable', help='path to YouTube DL')

    parser.add_argument('-x', help='audio only', action='store_true')

    parser.add_argument('--audio-format', help='e.g, wav')

    parser.add_argument('--ffmpeg-location', help='path to ffmpeg')

    parser.add_argument('url', help='YouTube URL', nargs=1)

    args = parser.parse_args()

    main(args)
