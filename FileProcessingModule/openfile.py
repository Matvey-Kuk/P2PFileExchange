import pickle

class diffile:
    """Поиск разницы между новой и старой версией. Пока статический"""
    def __init__(self):
        try:
            self.file = open('/example/text','rb').read()
            self.oldfile = open('/example/text2','rb').read()
        except IOError:
            print("No file")
        self.delta = {} #Блок данных для хранения разницы

    def save(self):#Запись разницы в фаил
        Close_file = open('/example/deltafile.txt', 'wb')
        pickle.dump(self.delta , Close_file)
        Close_file.close()

    def load(self):#Чтение разницы
        Open_file = open('/example/deltafile.txt', 'rb')
        delta = pickle.load(Open_file)
        print(delta)

    def find_diff(self):
        str_delta = []
        flag = 0
        for Read , oldRead , num in zip(self.file, self.oldfile, enumerate(self.file)):
            if(Read != oldRead):
                ho = chr(Read)
                str_delta.append(ho)
                flag = 1
            else:
                if(flag == 1):
                    self.delta[num[0]] = str_delta
                    str_delta = []
                flag = 0
        self.save()


if ("__name__" == "__main__"):
    dif = diffile()
    dif.find_diff()
    dif.load()