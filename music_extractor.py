import numpy as np
from pydub import AudioSegment
import librosa
from music21 import stream, note, midi

def mp3_to_wav(mp3_path, wav_path):
    audio = AudioSegment.from_mp3(mp3_path)
    audio.export(wav_path, format="wav")

# wav_path, none
def extract_pitches(y, sr):
    # Use librosa to detect pitches
    print("Use librosa to detect pitches")
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    
    # Extract the pitch values at each frame
    print("Extract the pitch values at each frame")
    pitch_values = []
    for t in range(pitches.shape[1]):
        index = magnitudes[:, t].argmax()
        pitch = pitches[index, t]
        if pitch > 0:
            pitch_values.append(pitch)
        else:
            pitch_values.append(None)
    
    return pitch_values

def convert_pitches_to_notes(pitch_values, sr, hop_length):
    # Convert pitch values to note objects
    print("Convert pitch values to note objects")
    note_stream = stream.Stream()
    prev_note = None
    duration = 0
    for i, pitch in enumerate(pitch_values):
        if pitch is not None:
            midi_note = librosa.hz_to_midi(pitch)
            if prev_note is None:
                prev_note = midi_note
                duration = 1
            elif prev_note == midi_note:
                duration += 1
            else:
                n = note.Note()
                n.pitch.midi = int(prev_note)
                n.quarterLength = duration * hop_length / sr
                note_stream.append(n)
                prev_note = midi_note
                duration = 1
        else:
            if prev_note is not None:
                n = note.Note()
                n.pitch.midi = int(prev_note)
                n.quarterLength = duration * hop_length / sr
                note_stream.append(n)
                prev_note = None
                duration = 0
    
    if prev_note is not None:
        n = note.Note()
        n.pitch.midi = int(prev_note)
        n.quarterLength = duration * hop_length / sr
        note_stream.append(n)
    
    return note_stream

def save_midi(note_stream, midi_path):
    mf = midi.translate.music21ObjectToMidiFile(note_stream)
    mf.open(midi_path, 'wb')
    mf.write()
    mf.close()
