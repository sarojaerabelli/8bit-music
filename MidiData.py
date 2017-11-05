"""Class for training example of a midi file."""
import numpy as np

class MidiData:

    def __init__(self, tempo, num_tracks):
        self.tempo = tempo
        self.num_tracks = num_tracks
        self.note_vectors = []
        self.TIME_STEP_SIZE = 0.001 # 10 ms

    def set_note_vectors(self, note_sequences):
        """Set self.note_vectors from a list of note sequences. Each vector will represent a
        second time interval containing a one-hot encoding of 128 note-on events and 128
        note-off events. TO BE DECIDED.

        Args:
           note_sequences: List of note sequences containing vector with track number,
           'note_on' or 'note_off', MIDI pitch, velocity, and duration of note in seconds.
        """
        note_on_list = [0] * 128
        note_off_list = [0] * 128
        time_step_list = [0] * 100
        tracks = [[] for _ in range(self.num_tracks)]

        for note_dir in note_sequences:
            if note_dir['type'] == 'note_on':
                note_on_list[note_dir['note']] = 1
            else:
                note_off_list[note_dir['note']] = 1
            time_shift = int(note_dir['time'] / self.TIME_STEP_SIZE)
            print(time_shift)
            time_step_list[time_shift] = 1
            vector = note_on_list + note_off_list + time_step_list
            tracks[note_dir['track']].append(vector)

        self.note_vectors = tracks
