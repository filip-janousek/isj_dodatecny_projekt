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
import threading
import multiprocessing
import time
from queue import Queue
###
### factorial calculation
### commented prints will output 1st 10 digits of factorials if uncommented
###
def factorial(n):
    if n == 0:
        return 1
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

# asyncio
async def compute_factorial_async(n):
    return factorial(n)

async def main_async(numbers):
    tasks = [compute_factorial_async(n) for n in numbers]
    return await asyncio.gather(*tasks)

# threading
def compute_factorial_threading(n):
    return factorial(n)

def worker():
    while True:
        cur_num, index = q.get()
        resultss[index] = compute_factorial_threading(cur_num)
        q.task_done()

def main_threading(numbers):
    global resultss
    resultss = [None] * len(numbers)
    for i in range(len(numbers)):
         t = threading.Thread(target=worker)
         t.daemon = True
         t.start()

    for index, item in enumerate(numbers):
        q.put((item, index))

    q.join()


# multiprocessing
def compute_factorial_multiprocessing(n):
    return factorial(n)

def main_multiprocessing(numbers):
    with multiprocessing.Pool() as pool:
        results = pool.map(compute_factorial_multiprocessing, numbers)
    return results

# main
if __name__ == "__main__":
    numbers = [1500] * 3000  # numbers we want factorials of, for demonstartion purposes same number 3000 times

    
    start_time = time.time() # time measuring - async

    print_pom = asyncio.run(main_async(numbers))
    print(f"Asyncio version took {time.time() - start_time} seconds\n")
    #print([str(num)[:10] for num in print_pom])
    
    

    start_time = time.time() # time measuring - threading
    q = Queue()
    resultss = []

    main_threading(numbers)
    print(f"Threading version took {time.time() - start_time} seconds\n")
    #print([str(num)[:10] for num in resultss])
    
    start_time = time.time() # time measuring - multiprocessing
    print_pom = main_multiprocessing(numbers)
    print(f"Multiprocessing version took {time.time() - start_time} seconds")
    #print([str(num)[:10] for num in print_pom])
   
