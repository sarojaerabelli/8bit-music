"""Class for training example of a midi file."""

class MidiData:

    def __init__(self, tempo, num_tracks):
        self.tempo = tempo
        self.num_tracks = num_tracks
        self.note_vectors = []

    def set_note_vectors(self, note_sequences):
        """Set self.note_vectors from a list of note sequences. Each vector will represent a
        second time interval containing a one-hot encoding of 128 note-on events and 128
        note-off events. TO BE DECIDED.

        Args:
           note_sequences: List of note sequences containing vector with track number,
           'note_on' or 'note_off', MIDI pitch, velocity, and duration of note in seconds.
        """
        self.note_vectors = note_sequences
