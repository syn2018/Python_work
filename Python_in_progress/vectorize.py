# coding: utf-8
#!/usr/bin/python
import thread
import time
# Define a function for the thread
def print_time(threadName, delay):
    count = 0 
    while count < 5:
        time.sleep(delay)
        count += 1 
        print "%s: %s" % (threadName, time.ctime(time.time()))
        
## Creating the threads
try:
    thread.start_new_thread(print_time, ("Thread-1", 2,))
    thread.start_new_thread(print_time, ("Thread-2", 4,))
exept:
try:
    thread.start_new_thread(print_time, ("Thread-1", 2,))
    thread.start_new_thread(print_time, ("Thread-2", 4,))
except:
    print "Error: unable to start thread" 
def print_time(threadName, delay):
    count = 0 
    while count < 5:
        time.sleep(delay)
        count += 1 
        print "%s: %s" % (threadName, time.ctime(time.time()))
        
import threading
import time
exitFlag = 0 
def print_time(threadName, delay):
    count = 0 
    while count < 5:
        time.sleep(delay)
        count += 1 
        print "%s: %s" % (threadName, time.ctime(time.time()))
        
import threading
l
get_ipython().magic(u'save vectorize.py 1-16')
