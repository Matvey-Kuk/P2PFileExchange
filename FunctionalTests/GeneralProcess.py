import subprocess
import tempfile
import threading


arr = {}

processes = []


def creation_process(n):
    global arr
    for i in range(n):
        f = tempfile.TemporaryFile()
        #f = open('text.txt', 'a')
        subprocess.Popen(['python3 $HOME/network/Main.py -h'], stdout=f, shell=True)
        processes.append(f)
        arr[i] = f



def log():
    global arr
    while True:
        n=int(input("Введите номер экземпляра запущенной программы:"))
        arr[n-1].seek(0)
        print(arr[n-1].read())


t1 = threading.Thread(name='th1', target=creation_process, kwargs={'n': 10})
t2 = threading.Thread(name='th2', target=log)

t1.start()
t2.start()