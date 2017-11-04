"""Code for transforming midi files into one-hot vectors."""

import mido
import os
import matplotlib.pyplot as plt
import numpy as np
from MidiData import MidiData

def get_note_sequences(midi, tempo):
    """Get note sequences from a midi file.

    Args:
       midi: MidiFile object.
       
    Returns:
        List of note sequences.
    """
    note_sequences = []

    for i, track in enumerate(midi.tracks):
        for msg in track:               
            if not msg.is_meta:
                note_vector = {}
                # Convert tiem to seconds.
                time = mido.tick2second(msg.time, midi.ticks_per_beat, tempo)
                if msg.type == 'note_on' or msg.type == 'note_off':
                    # Get note value.
                    msg_str = str(msg)
                    start = msg_str.index('note=')
                    new_msg = msg_str[start + 5:]
                    end = new_msg.index(' ')
                    note = int(new_msg[:end])

                    # Get velocity value.
                    start = msg_str.index('velocity=')
                    new_msg = msg_str[start + 9:]
                    end = new_msg.index(' ')
                    velocity = int(new_msg[:end])

                    # Set note vector values.
                    note_vector["track"] = i
                    note_vector["type"] = msg.type
                    note_vector["note"] = note
                    note_vector["velocity"] = velocity
                    note_vector["time"] = time

                    # Add note vector to note sequence list.
                    note_sequences.append(note_vector)

    return note_sequences

def get_midi_data(tempo, num_tracks, note_sequences):
    """Get MidiData object from a list of note sequences.

    Args:
       tempo: Integer describing tempo.
       num_tracks: Number of tracks in midi.
       note_sequences: List of note sequences containing vector with track number,
       'note_on' or 'note_off', MIDI pitch, velocity, and duration of note in seconds.
       
    Returns:
        MidiData object containing training vector sequence.
    """
    midi_data = MidiData(tempo, num_tracks)
    midi_data.set_note_vectors(note_sequences)
    return midi_data

def process_midi_file(midi_file, max_num_tracks=5):
    """Get MidiData object from midi_file.

    Args:
       midi_file: Filename.
       max_num_tracks: Maximum possible tracks for our desired midi files.
       
    Returns:
        MidiData object containing training vector sequence.
    """
    mid = mido.MidiFile(midi_file)

    # Only include file if it has few enough tracks.
    if len(mid.tracks) > max_num_tracks:
        return None

    # Find tempo.
    for i, track in enumerate(mid.tracks):
        for msg in track:
            if msg.is_meta and msg.type == 'set_tempo':
                msg_str = str(msg)
                start = msg_str.index('tempo=')
                new_msg = msg_str[start + 6:]
                end = new_msg.index(' ')
                tempo = int(new_msg[:end])

    note_sequences = get_note_sequences(mid, tempo)
    return get_midi_data(tempo, len(mid.tracks), note_sequences)


def examine_track_count():
    """Plots the distribution of the number of tracks in 'midis' directory.
    """
    count = 0
    num_tracks = []
    for filename in os.listdir('midis/'):
        if filename.endswith(".mid"):
            count += 1
            print(count)
            print(filename)
            mid = mido.MidiFile('midis/' + midi_file)
            num_tracks.append(len(mid.tracks))

    plt.hist(num_tracks, count)
    plt.show()

def main():
    midi_file = 'midis/3D_Worldrunner_Bonus.mid'
    m = process_midi_file(midi_file)
    print(m.tempo)
    print(m.num_tracks)
    print(m.note_vectors)

if __name__ == '__main__':
    main()