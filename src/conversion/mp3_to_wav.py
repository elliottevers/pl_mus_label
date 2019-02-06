from pydub import AudioSegment
from os import remove as rm_os

# TODO: add exception handling

# do not escape spaces with forward slashes like at the shell

filename = '/Users/elliottevers/Documents/git-repos.nosync/music/output/tk_music/Creedence Clearwater Revival - Lodi'

extension_wav = 'wav'

extension_mp3 = 'mp3'

sound = AudioSegment.from_mp3(filename + '.' + extension_mp3)

sound.export(filename + '.' + extension_wav, format="wav")

rm_os(filename + '.' + extension_mp3)

