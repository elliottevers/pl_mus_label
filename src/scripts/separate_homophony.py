import sys
sys.path.insert(0, '/Users/elliottevers/Documents/git-repos.nosync/tk_music_py/src')
from message import messenger as mes
import argparse
from utils import utils
from i_o import importer as io_importer, exporter as io_exporter
from convert import music_xml as convert_mxl
from postprocess import music_xml as postp_mxl


def main(args):

    name_part = 'homophony'

    importer = io_importer.Importer(
        utils.get_file_json_comm()
    )

    importer.load([name_part])

    notes_live = importer.get_part(name_part)

    (
        s_beat_start,
        s_beat_end,
        tempo,
        beat_start,
        beat_end,
        length_beats,
        beatmap
    ) = utils.get_tuple_beats()

    messenger = mes.Messenger()

    messenger.message(['length_beats', str(length_beats)])

    stream = convert_mxl.live_to_stream(
        notes_live,
        beatmap=beatmap,
        s_beat_start=s_beat_start,
        s_beat_end=s_beat_end,
        tempo=tempo,
        mode='polyphonic'
    )

    part_textured = postp_mxl.force_texture(stream, int(args.desired_texture.replace('"', '')))

    part_voice_extracted = postp_mxl.extract_voice(part_textured, 1)

    notes_live = convert_mxl.to_notes_live(
        part_voice_extracted,
        beatmap=beatmap,
        s_beat_start=s_beat_start,
        s_beat_end=s_beat_end,
        tempo=tempo,
        bypass_seconds=True
    )

    exporter = io_exporter.Exporter()

    exporter.set_part(notes_live, name_part)

    exporter.export(utils.get_file_json_comm())

    messenger.message(['done', 'bang'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Separate voices from homophony')

    parser.add_argument('--desired_texture', help='number of voices to force MIDI to have')

    parser.add_argument('--index_voice', help='which voice to extract')

    args = parser.parse_args()

    main(args)
