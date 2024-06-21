from music_parser import *
from roboid import *
from note import code
import asyncio

def distribute_tasks(n, tasks):
    # n개의 부저 리스트 초기화
    buzzers = [[] for _ in range(n)]
    available_time = [0] * n  # 각 부저의 사용 가능 시간 초기화

    # 주어진 작업을 시작 시간에 맞춰 부저에 분배
    for task in tasks:
        hertz, duration, start_time = task
        # 가장 먼저 작업을 수행할 수 있는 부저 찾기
        for i in range(n):
            if available_time[i] <= start_time:
                buzzers[i].append(task)
                available_time[i] = start_time + duration  # 부저의 사용 가능 시간 업데이트
                break
    
    return buzzers

async def avant_song(n, music_name):
    tasks = []
    muse = parse_music_ultimate(music_name)
    result = distribute_tasks(n, muse)
    
    for i in range(n):
        print("task started", i)
        for j in range(len(result[i])):
            tasks.append(song(i, [result[i][j]]))
    await asyncio.gather(*tasks)



async def song(index, task):
    cur_time = task[0][2]
    await asyncio.sleep(cur_time)
    for pitch, duration, start_time in task:
        await asyncio.sleep(start_time - cur_time)
        print(f"index : {index}, pitch : {pitch}, duration : {duration}, start_time : {start_time}, wait_time : {start_time - cur_time}")
        hamster[index].note(code[pitch])
        await asyncio.sleep(duration)
        cur_time = start_time + duration
        hamster[index].note(0)

n = 3

# file_name = "Summer - Joe Hisaishi"
file_name = "flowerdance - djokawari"
muse = parse_music_ultimate(file_name)
result = distribute_tasks(n, muse)

hamster = []  
for i in range(3):
    hamster.append(Hamster(i))
    hamster[i].tempo(60)

import time

# print(time.time())


asyncio.run(avant_song(n, file_name))
# avant_song2(n, file_name)

# hamster[0].note(code["E-5"])