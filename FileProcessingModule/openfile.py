import pickle
<<<<<<< HEAD

class diffile:
    def __init__(self):
        try:
            self.file = open('/home/lossidze/test/text','rb').read()
        except IOError:
            print("No file")
        self.oldfile = open('/home/lossidze/test/text2','rb').read()
        self.delta = {}

    def save(self):
        Close_file = open('/home/lossidze/test/deltafile.txt', 'wb')
        pickle.dump(self.delta , Close_file)
        Close_file.close()

    def load(self):
        Open_file = open('/home/lossidze/test/deltafile.txt', 'rb')
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


#if ("__name__" == "__main__"):
dif = diffile()
dif.find_diff()
dif.load()
=======
from OpenDir import OpenDir
import os


class Diffile:
    def __init__(self, path):
        self.take_dir = OpenDir(path)

    def take_files(self):
        for keys in self.take_dir.files_in_dir.keys():
            for items in self.take_dir.files_in_dir[keys]:
                if os.path.exists('system/' + items):
                    delta = self.find_diff(keys + '/' + items, 'system/' + items + '/' + items)
                    if len(delta.keys()) != 0:
                       self.save('system/' + items, delta, keys + '/' + items, '/' + items)
                else:
                    os.mkdir('system/' + items)
                    newfile = open('system/' + items + '/' + items, 'wb')
                    newfile.write(open(keys + '/' + items, 'rb').read())
                    newfile.close()

    def find_diff(self, path_file, path_store_file):
        file = open(path_file, 'rb').read()
        oldfile = open(path_store_file, 'rb').read()
        str_delta = []
        delta = {}
        flag = 0
        for oldRead, Read in zip(oldfile, enumerate(file)):
            if(Read[1] != oldRead):
                ho = chr(oldRead)
                str_delta.append(ho)
                flag += 1
            else:
                if(flag != 0):
                    delta[Read[0]-flag] = str_delta
                    str_delta = []
                flag = 0
        if(len(oldfile) > len(file)):
            delta[len(file)-1] = oldfile[len(file)-1:len(oldfile)-1]
        if(len(oldfile) < len(file)):
            delta['last'] = len(oldfile)
        return delta

    def save(self, path, delta, path_newfile, path_oldfile):
            local = os.listdir(path)
            delta_file = open(path + '/_delta' + str(len(local)-1), 'wb')
            pickle.dump(delta, delta_file)
            delta_file.close()
            newfile = open(path_newfile, 'rb').read()
            open(path + path_oldfile, 'wb').write(newfile)

    def back_step(self):
        for keys in self.take_dir.files_in_dir.keys():
            for items in self.take_dir.files_in_dir[keys]:
                print(items)

    def load(self):
        Open_file = open('system/text.txt/_delta0', 'rb')
        delta = pickle.load(Open_file)
        print(delta)

test = Diffile('base')
test.take_files()
test.back_step()
"""




dif = diffile()
dif.find_diff()
"""
>>>>>>> Cotl
