import os

class OpenDir():
    def __init__(self):
        self.files_in_dir = {}
    def see_dir(self, path):
        try:
            self.files_in_dir[path] = os.listdir(path)
        except:
            return False
        else:
            for i, file in enumerate(self.files_in_dir[path]):
                if(self.see_dir(path + '/' + file) == True):
                    del self.files_in_dir[path][i]
                    if len(self.files_in_dir[path]) == 0 :
                        del self.files_in_dir[path]
            return True

test = OpenDir()
test.see_dir('base')
print(test.files_in_dir)