from music_parser import *
from music_extractor import *
from note import code
from roboid import *
from music21 import *
import asyncio

import time

def note_to_string(note):
    return note.name + str(note.octave)


def avant_song(music_name):
    muse = parse_music_core_dual(music_name)
    for e, duration in muse:
        asyncio.run(do_song(e, duration))
    
    
# 비동기
async def do_song(c, note_time):
    tasks = []
    for i in range( min( len(c), len(hamster) ) ):
        print(c[i], note_time)
        notee = code[c[i]]
        tasks.append(hamster_note_async(i, notee, note_time))
    await asyncio.gather(*tasks)

async def hamster_note_async(index, note, note_time):
    hamster[index].note(note)
    await asyncio.sleep(note_time)
    hamster[index].note(0)


hamster = []  
for i in range(2):
    hamster.append(Hamster(i))
    hamster[i].tempo(60)

if __name__ == "__main__":
    # file_name = "Undertale_-_Megalovania"
    # file_name = "Undertale_-_Spear_Of_Justice"
    file_name = "Summer - Joe Hisaishi"
    # parse_music("./"+file_name+".mid")
    
    avant_song(file_name)
    # parse(file_name)
    print("heeloo world")
