import youtube_dl
import subprocess, os
output_dir = '/Users/elliottevers/Documents/git-repos.nosync/audio/youtube'
output_file = 'teardrops_tswift'
output_format = 'wav'
url = 'https://www.youtube.com/watch?v=CbkvLYrEvF4'
cmd = f"youtube-dl -x --audio-format {output_format} -o {output_dir}/{output_file}.%(ext)s {url}"
subprocess.run(cmd.split())
