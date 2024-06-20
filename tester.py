from music_parser import *
from roboid import *
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
        tasks.append(song(i, result[i]))
    await asyncio.gather(*tasks)



async def song(index, task):
    cur_time = 0
    for hertz, duration, start_time in task:
        await asyncio.sleep(start_time - cur_time)
        cur_time = start_time
        print(f"index : {index}, hertz : {hertz}, duration : {duration}, start_time : {start_time}, wait_time : {start_time - cur_time}")
        hamster[index].note(hertz)
        await asyncio.sleep(duration)
        cur_time += duration
        hamster[index].note(0)

n = 3

file_name = "Summer - Joe Hisaishi"

muse = parse_music_ultimate(file_name)
result = distribute_tasks(n, muse)

hamster = []  
for i in range(3):
    hamster.append(Hamster(i))
    hamster[i].tempo(60)
    
asyncio.run(avant_song(n, file_name))
# avant_song2(n, file_name)