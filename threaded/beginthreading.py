#!/usr/bin/env python
#simple code which uses threads

import time
from threading import Thread

class MyThread(Thread):

    def __init__(self,bignum):

        Thread.__init__(self)
        self.bignum=bignum
    def printMsg(self,numIn):
	print "Test " + str(numIn)
    def run(self):

        for l in range(10):
            for k in range(self.bignum):
                res=0
                for i in range(self.bignum):
		    self.printMsg(res)
                    res+=1


def test():
    bignum=1000
    thr1=MyThread(bignum)
    thr1.start()
    thr1.join()
    
if __name__=="__main__":
    test()
