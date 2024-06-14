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
import aiohttp
import threading
import requests
import multiprocessing
import time
from bs4 import BeautifulSoup
from queue import Queue
###
### get h1 content from website
### commented prints will output results if uncommented
###



# asyncio
async def fetch_title_async(session, url):
    async with session.get(url) as response:
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')
        h1_tag = soup.find('h1')
        return h1_tag.text if h1_tag else 'No h1 element present' 

async def main_async(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_title_async(session, url) for url in urls]
        return await asyncio.gather(*tasks)

# threading

def fetch_title_threading(url):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    h1_tag = soup.find('h1')
    return h1_tag.text if h1_tag else 'No h1 element present' 

def worker():
    while True:
        cur_url, index = q.get()
        resultss[index] = fetch_title_threading(cur_url)
        q.task_done()

def main_threading(urls):
    global resultss
    resultss = [None] * len(urls)
    for i in range(len(urls)):
         t = threading.Thread(target=worker)
         t.daemon = True
         t.start()

    for index, item in enumerate(urls):
        q.put((item, index))

    q.join()


# multiprocessing
def fetch_title_multiprocessing(url):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    h1_tag = soup.find('h1')
    return h1_tag.text if h1_tag else 'No h1 element present' 

def main_multiprocessing(urls):
    with multiprocessing.Pool() as pool:
        results = pool.map(fetch_title_multiprocessing, urls)
    return results

if __name__ == "__main__":
    urls = [
        'https://www.google.com/',
        'https://www.vut.cz/',
        'https://github.com/',
        'https://www.youtube.com/'
    ] # list of websites from which we want h1 content

     
    start_time = time.time() # time measuring - async

    print_pom = list(asyncio.run(main_async(urls)))
    print(f"\nAsyncio version took {time.time() - start_time} seconds")
    #print(print_pom)
    


    start_time = time.time() # time measuring - threading
    q = Queue()
    resultss = []
    main_threading(urls)
    print(f"\nThreading version took {time.time() - start_time} seconds")
    #print(resultss)
    
  
    start_time = time.time() # time measuring - multiprocessing
    print_pom = main_multiprocessing(urls)
    
    print(f"\nMultiprocessing version took {time.time() - start_time} seconds")
    #print(print_pom)
