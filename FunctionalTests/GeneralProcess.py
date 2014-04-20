import subprocess
import os
import tempfile
import threading
from time import sleep

arr = {}

processes = []


def creation_process(n):
    global arr
    for i in range(n):
        f = tempfile.TemporaryFile()
        #f = open('text.txt', 'a')
        subprocess.Popen(['python3', 'TestScript.py', str(i)], stdout=f)
        processes.append(f)
        arr[i] = f
        #print(arr[i])
        #sleep(0.03)
        #arr[i].seek(0)
        #print(arr[i].read())
        #sleep(0.025)

"""while True:
    for f in processes:
        f.seek(0)
        print(f.read())
    sleep(1)"""

#sleep(0.03)


def log():
    sleep(2)
    print("!")
    for r in arr:
        arr[r].seek(0)
        print(arr[r].read())


t1 = threading.Thread(name='th1', target=creation_process, kwargs={'n': 3})
t2 = threading.Thread(name='th2', target=log)

t1.start()

t2.start()