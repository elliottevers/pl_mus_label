import subprocess

# output_dir = '/Users/elliottevers/Documents/git-repos.nosync/audio/youtube'
# output_file = 'teardrops_tswift'
# output_format = 'wav'
# url = 'https://www.youtube.com/watch?v=CbkvLYrEvF4'
# cmd = f"youtube-dl -x --audio-format {output_format} -o {output_dir}/{output_file}.%(ext)s {url}"


def run(argv):
    # subprocess.run(cmd.split())
    # print(argv)
    output_dir = '/Users/elliottevers/Documents/git-repos.nosync/audio/youtube'
    output_file = 'teardrops_tswift'
    output_format = 'wav'
    url = 'https://www.youtube.com/watch?v=CbkvLYrEvF4'
    cmd = f"/usr/local/bin/youtube-dl -x --audio-format {output_format} -o {output_dir}/{output_file}.%(ext)s {url}"
    print(argv)
    subprocess.run(cmd.split())


if __name__ == '__main__':
    import sys
    # cmd = sys.argv[1]
    run(sys.argv)
