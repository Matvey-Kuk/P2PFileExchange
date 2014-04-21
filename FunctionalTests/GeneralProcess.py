import subprocess
import tempfile
import threading


arr = {}

processes = []

#Не информативное название переменной
k = int(input("Какое количество программ запустить:"))

#Todo: Получать это через аргументы командной строки
program_path = input("Путь к папке с приложением:")


def creation_process():
    global arr
    for i in range(k):
        f = tempfile.TemporaryFile()
        #f = open('text.txt', 'a')
        if i == 0:
            subprocess.Popen(
                ['python3 ' + program_path + '/Main.py -port 111' + str(i+1) + ' -P2PModule'],
                stdout=f,
                shell=True
            )
        else:
            subprocess.Popen(
                ['python3 ' + program_path + '/Main.py -port 111' + str(i+1) + ' -peer 127.0.0.1:111' + str(i + 1) +
                 ' -P2PModule'],
                stdout=f,
                shell=True
            )
        processes.append(f)
        arr[i] = f


def log():
    global arr
    while True:
        n = int(input("Введите номер экземпляра запущенной программы:"))
        arr[n-1].seek(0)
        print(arr[n-1].read())


t1 = threading.Thread(name='th1', target=creation_process)
t2 = threading.Thread(name='th2', target=log)

t1.start()
t2.start()