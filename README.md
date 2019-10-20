This is the information retrieval component of an ambitious ear training library - it's main function is to estimate high-level musical information such as beat, key centers, chords, bass, melody directly from raw audio.  Video demos of the project can be seen [here](https://elliottevers.github.io/).

Remote Debugging:

- use `easy_install` to install Python 3 `pycharm-debug` egg inside PyCharm distribution
- put the following lines in script
```
import pydevd
pydevd.settrace('localhost', port=8008, stdoutToServer=True, stderrToServer=True)
```
- run script with Max


Environment:

uses the interpreter at `/Users/elliottevers/DocumentsTurbulent/venvwrapper/requirements_tk_music/bin/python` managed by `virtualenvwrapper`