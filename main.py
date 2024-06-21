from music_parser import *
from roboid import *
from note import code
import asyncio

def distribute_tasks(n, tasks):
    # 간단한 태스크 스케줄링
    # n개의 햄스터(부저) 리스트 초기화
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
    # 노래 시행
    tasks = []
    muse = parse_music_ultimate(music_name)
    result = distribute_tasks(n, muse)
    
    for i in range(n):
        print("task started", i)
        for j in range(len(result[i])):
            # note 하나 단위로 넣어줌.
            tasks.append(song(i, [result[i][j]]))
    await asyncio.gather(*tasks)



async def song(index, task):
    # 원래 리스트로 받아서 해당 인덱스 햄스터가 시간에 맞춰 연주하는 방식인데, 태스크의 길이가 길수록 싱크가 안맞아 하나씩만 넣어주었다.
    # 하나만 받아서 더 짧게 할 수 있지만 이래야 싱크가 맞는다... 도대체 왜???
    # 햄스터 문제로 보인다...
    cur_time = task[0][2]
    # 시작 전 노트시간 동기화
    await asyncio.sleep(cur_time)
    # pitch(음계), duration(음표길이), start_time(시작시간)
    for pitch, duration, start_time in task:
        # cur_time과 start_time 비교해서 기다리는 시간 계산 후 기다리는 건데 task가 하나만 주어져서 의미없는 코드다.
        await asyncio.sleep(start_time - cur_time)
        print(f"index : {index}, pitch : {pitch}, duration : {duration}, start_time : {start_time}, wait_time : {start_time - cur_time}")
        # 음계에 맞는 햄스터 상수가 딕셔너리형태(code)로 매핑되어있다. 해당 상수를 불러와 note()에 입력해준다.
        hamster[index].note(code[pitch])
        await asyncio.sleep(duration)
        # duration 동안 기다림
        cur_time = start_time + duration
        # 연주 종료 및 cur_time 갱신
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


asyncio.run(avant_song(n, file_name))