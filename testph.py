#!/usr/bin/python3.2
from threading import Thread
import time 
class race(Thread):
    def __init__(self,threadname, interval):
        Thread.__init__(self,name = threadname)
        self.interval = interval
        self.isrunning = True


    def run(self):
        while self.isrunning:
            print ('thread %s is running, time: %s\n' %(self.getName(), time.ctime()))
            time.sleep(self.interval)

    def stop(self):
        self.isrunning = False

def test():
	i = 0
	thead1 = race('A',1)
	thead2 = race('B',1)
	thead1.start()
	thead2.start()

	thead_list.put(thead1)
	#thead1.join()
	#thead2.join()
	time.sleep(5)
	thead1.stop()
	thead2.stop()

if __name__ == '__main__':
    test()
