#!/usr/bin/python3.2
import threading
from queue import Queue
import time

#lock to serialize console output
lock = threading.Lock()

def do_work(item, item2 = 3):
	time.sleep(.1)
	with lock:
		print(threading.current_thread().name, item)

#The worker thread pulls an item from the queue and process it
def worker():
	while True:
		item = q.get()
		#print ("item:",item[0])
		do_work(item)
		q.task_done()

#Create the queue and thread pool
q = Queue()
for i in range(4):
	t = threading.Thread(target=worker)
	t.daemon = True
	t.start()

#stuff work items on the queue(in this case, just a nember)
#start = time.perf_counter()
for item in range(20):
	#print (item)
	q.put((item, 3))

q.join()
