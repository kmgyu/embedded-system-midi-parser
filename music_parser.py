from music21 import *

def parse_music_ultimate(midi_path):
    # midi 파일 파싱
    # 최종 메서드
    midi = converter.parse("./"+midi_path+".mid")
    # 파싱된 노트들만 가져옴
    notes_to_parse = midi.flat.notes
    
    result = []
    for e in notes_to_parse:
        # note (한개 음표)인 경우
        if isinstance(e, note.Note):
            core_note = e.pitch.name + str(e.pitch.octave)
            result.append([core_note, e.duration.quarterLength, e.offset])
        # chord (여러 음표)인 경우
        elif isinstance(e, chord.Chord):
            for p in e.pitches:
                result.append([p.name + str(p.octave), e.duration.quarterLength, e.offset])
    return result