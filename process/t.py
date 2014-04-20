import threading
import time
import os

def f(a, b, c):
    while True:
        print("Я первый поток и запускаю " + str(a))
        os.system("python3 script0.py " + str(a))
        time.sleep(4)

s = []
for i in range(10):
    s.append(threading.Thread(name='th1', target=f, args=(i, 2), kwargs={'c': 3}))

for thread in s:
    thread.start()
