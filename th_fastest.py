#!/usr/bin/python3
########################################
# added directory with external libries to sys.path in case they are not instaleld on machide
#import sys
#from pathlib import Path
#script_dir = Path(__file__).resolve().parent
#libs_dir = script_dir / 'libs'
#sys.path.append(str(libs_dir))
########################################
import asyncio
import aiofiles
import threading
import multiprocessing
import time
from queue import Queue


###
### get 1st line from selected files
### commented prints will output 1st 1st line from selected files if uncommented
###



# asyncio
async def read_file_async(file_path):
    async with aiofiles.open(file_path, 'r', encoding='utf-8') as file:
        return await file.readline()

async def main_async(file_paths):
    tasks = [read_file_async(file_path) for file_path in file_paths]
    return await asyncio.gather(*tasks)


# threading
def read_file_threading(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readline()
    
def worker():
    while True:
        cur_file, index = q.get()
        resultss[index] = read_file_threading(cur_file)
        q.task_done()

def main_threading(file_paths):
    global resultss
    resultss = [None] * len(file_paths)
    for i in range(len(file_paths)):
         t = threading.Thread(target=worker)
         t.daemon = True
         t.start()

    for index, item in enumerate(file_paths):
        q.put((item, index))

    q.join()

# multiprocessing
def read_file_multiprocessing(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readline()

def main_multiprocessing(file_paths):
    with multiprocessing.Pool() as pool:
        results = pool.map(read_file_multiprocessing, file_paths)
    return results

if __name__ == "__main__":
    file_paths = ['small_file.txt'] * 100   # files we want to get 1st line from, for demonstartion purposes same file 100 times

    start_time = time.time() # time measuring - async
    print_pom = asyncio.run(main_async(file_paths))
    print(f"\nAsyncio version took {time.time() - start_time} seconds")
    #print(print_pom)

    start_time = time.time() # time measuring - threading
    q = Queue()
    resultss = []
    main_threading(file_paths)
    print(f"\nThreading version took {time.time() - start_time} seconds")
    #print(resultss)

    start_time = time.time() # time measuring - multiprocessing
    print_pom = main_multiprocessing(file_paths)
    print(f"\nMultiprocessing version took {time.time() - start_time} seconds")
    #print(print_pom)
