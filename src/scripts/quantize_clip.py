from message import messenger as mes
import argparse
from utils import utils
from i_o import importer as io_importer, exporter as io_exporter
from convert import music_xml as convert_mxl


def main(args):

    name_part = args.name_part.replace("\"", '')

    beat_multiple_quantization = args.beat_multiple.replace("\"", '')

    quarter_length_divisor = 1/float(beat_multiple_quantization)

    importer = io_importer.Importer(
        utils.get_file_json_comm()
    )

    importer.load([name_part])

    notes_live = importer.get_part(name_part)

    # convert ableton live notes to stream

    from postprocess import music_xml as postp_mxl

    mode = 'polyphonic' if name_part == 'chord' else 'monophonic'

    stream = postp_mxl.live_to_stream(
        notes_live,
        mode
    )

    from music import song

    if name_part == 'melody':

        import os
        import librosa
        # from information_retrieval import extraction as ir
        from preprocess import vamp as prep_vamp

        y, sr = librosa.load(
            os.path.join(
                utils.get_dirname_audio_warped(),
                utils._get_name_project_most_recent() + '.wav'
            )
        )

        duration_s_audio = librosa.get_duration(
            y=y,
            sr=sr
        )

        beat_start_marker, beat_end_marker, beat_loop_bracket_lower, beat_loop_bracket_upper, length_beats, beatmap = utils.get_tuple_beats(
            os.path.join(
                utils.get_dirname_beat(),
                utils._get_name_project_most_recent() + '.pkl'
            )
        )

        # messenger.message(['length_beats', str(length_beats)])

        s_beat_start = (beat_start_marker / length_beats) * duration_s_audio

        s_beat_end = (beat_end_marker / (length_beats)) * duration_s_audio

        # NB: chords from raw audio
        # data_melody = ir.extract_segments(
        #     os.path.join(
        #         utils.get_dirname_audio_warped(),
        #         utils._get_name_project_most_recent() + '.wav'
        #     )
        # )

        from convert import vamp as conv_vamp

        data_melody = conv_vamp.to_data_melody(
            notes_live,
            offset_s_audio=0,
            duration_s_audio=177.15
        )

        mesh_song = song.MeshSong()

        df_melody = prep_vamp.melody_to_df(
            (data_melody['vector'][0], data_melody['vector'][1]),
            index_type='s'
        )

        df_melody[df_melody['melody'] < 0] = 0

        # df_melody = prep_vamp.melody_to_df(
        #     data_melody
        # )

        melody_tree = song.MeshSong.get_interval_tree(
            df_melody
        )

        mesh_song.set_tree(
            melody_tree,
            type='melody'
        )

        mesh_song.quantize(
            beatmap,
            s_beat_start,
            s_beat_end,
            beat_start_marker,  # transitioning indices here
            columns=['melody']
        )

        data_quantized_melody = mesh_song.data_quantized['melody']

        score = postp_mxl.df_grans_to_score(
            data_quantized_melody,
            parts=['melody']
        )

        stream = postp_mxl.extract_part(
            score,
            'melody'
        )
    else:
        stream.quantize(
            (quarter_length_divisor, ),
            inPlace=True
        )

    notes_live = convert_mxl.to_notes_live(
        stream
    )

    exporter = io_exporter.Exporter()

    exporter.set_part(notes_live, name_part)

    exporter.export(utils.get_file_json_comm())

    messenger = mes.Messenger()

    messenger.message(['done'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Quantize Chords')

    parser.add_argument('--beat_multiple', help='e.g., if 4, quantize to the measure')

    parser.add_argument('--name_part', help='e.g., if 4, quantize to the measure')

    args = parser.parse_args()

    main(args)
