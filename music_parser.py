from music21 import *
import numpy as np

def parse(midi_path):
    midi = converter.parse("./"+midi_path+".mid")
    midi.show("midi")

def to_midi():
    # 1. MIDI 파일 로드
    midi_file = converter.parse('path_to_your_midi_file.mid')

    # 2. 음계 분석
    main_key = midi_file.analyze('key')
    print("The key of this MIDI file is:", main_key)

    # 주어진 음계의 음들 가져오기
    scale_pitches = np.array([p.name for p in main_key.getScale().pitches])

    # 3. 음표의 이름을 NumPy 배열로 추출
    notes = [n for n in midi_file.flat.notes if isinstance(n, note.Note)]
    note_names = np.array([n.name for n in notes])

    # 4. NumPy 브로드캐스팅을 사용하여 음계에 해당하는 음들만 필터링
    mask = np.isin(note_names, scale_pitches)
    core_notes = np.array(notes)[mask]

    # 추출한 음들을 새로운 스트림에 추가
    core_stream = stream.Stream()
    for cn in core_notes:
        core_stream.append(cn)

    # 핵심 음들을 MIDI 파일로 저장
    core_stream.write('midi', fp='core_notes_output.mid')

    print("The core notes have been extracted and saved to 'core_notes_output.mid'.")

def parse_music(midi_path):
    midi = converter.parse("./"+midi_path+".mid")
    notes_to_parse = midi.flat.notes
    # midi.show()
    # notes_to_parse.show("text")
    cur_time = 0
    time = 0
    left = []
    right = []
    
    even = False
    
    for e in notes_to_parse:
        if e.offset-cur_time:
            time = e.offset-cur_time
        # print(e.offset, e.quarterLength, e.volume.velocity, e.volume.client)
        if e.isNote:
            if e.octave >= 4:
                right.append([e, time])
            else:
                left.append([e, time])
        elif e.isChord:
            l_chord = []
            r_chord = []
            for n in e:
                if n.octave >= 4:
                    l_chord.append(n)
                else:
                    r_chord.append(n)
            # if l_chord:
            #     left.append([l_chord, time])
            # if r_chord:
            #     right.append([r_chord, time])
            if l_chord:
                left.append([l_chord[0], time])
            if r_chord:
                right.append([r_chord[0], time])
        elif e.isRest:
            if even:
                right.append(["rest", e])
            else:
                left.append(["rest", e])
        cur_time = e.offset
    return left, right

def parse_music_upper(midi_path):
    midi = converter.parse("./"+midi_path+".mid")
    notes_to_parse = midi.flat.notes
    # midi.show()
    # notes_to_parse.show("text")
    cur_time = 0
    time = 0
    left = []
    right = []
    
    for e in notes_to_parse:
        
        if e.offset-cur_time:
            time = e.offset-cur_time
        # print(e.offset, e.quarterLength, e.volume.velocity, e.volume.client)
        if e.isNote:
            if e.octave >= 4:
                right.append([e, time])
        elif e.isChord:
            l_chord = []
            for n in e:
                if n.octave >= 4:
                    l_chord.append(n)
                if len(l_chord) >= 2: break
            # if l_chord:
            #     left.append([l_chord, time])
            # if r_chord:
            #     right.append([r_chord, time])
            if l_chord:
                left.append([l_chord.pop(), time])
                if l_chord:
                    right.append([l_chord.pop(), time])
        elif e.isRest:
            left.append(["rest", e])
            right.append(["rest", e])
        cur_time = e.offset
    return left, right

def parse_music_core(midi_path):
    midi = converter.parse("./"+midi_path+".mid")
    notes_to_parse = midi.flat.notes
    cur_offset = 0
    
    result = []
    for e in notes_to_parse:
        if e.offset == cur_offset:
            continue
        # print(e, e.duration.quarterLength )
        if isinstance(e, note.Note):
            if e.octave >= 4:
                result.append([e.pitch.name + str(e.pitch.octave), e.duration.quarterLength])
        elif isinstance(e, chord.Chord):
            if e.pitches[0].octave >= 4:
                result.append([e.pitches[0].name + str(e.pitches[0].octave), e.duration.quarterLength])
        cur_offset = e.offset
    return result
    

def parse_music_core_dual(midi_path):
    midi = converter.parse("./"+midi_path+".mid")
    notes_to_parse = midi.flat.notes
    cur_offset = 0
    
    result = []
    for e in notes_to_parse:
        if e.offset == cur_offset:
            continue
        # print(e, e.duration.quarterLength )
        if isinstance(e, note.Note):
            if e.octave <= 4:
                core_note = e.pitch.name + str(e.pitch.octave)
                result.append([[core_note], e.duration.quarterLength])
        elif isinstance(e, chord.Chord):
            sub = []
            for p in e.pitches:
                if p.octave <= 4:
                    sub.append([p.name, p.octave])
            if not sub: continue
            sub.sort(key=lambda x: x[1])
            core_note = sub[0][0] + str(sub[0][1])
            sub_note = sub[-1][0] + str(sub[-1][1])
            result.append([[core_note, sub_note], e.duration.quarterLength])
        cur_offset = e.offset
    return result

def parse_music_ultimate(midi_path):
    midi = converter.parse("./"+midi_path+".mid")
    notes_to_parse = midi.flat.notes
    # cur_offset = 0
    
    result = []
    for e in notes_to_parse:
        if isinstance(e, note.Note):
            core_note = e.pitch.name + str(e.pitch.octave)
            result.append([core_note, e.duration.quarterLength, e.offset])
        elif isinstance(e, chord.Chord):
            # sub = []
            for p in e.pitches:
                result.append([p.name + str(p.octave), e.duration.quarterLength, e.offset])
    return result