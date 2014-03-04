import pickle

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