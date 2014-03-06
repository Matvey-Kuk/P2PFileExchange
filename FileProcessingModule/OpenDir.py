import os


class OpenDir():
    def __init__(self, path):
        self.files_in_dir = {}
        self.see_dir(path)

    def see_dir(self, path):
        try:
            self.files_in_dir[path] = [x for x in os.listdir(path) if x[-1] != '~']
        except NotADirectoryError:
            return False
        else:
            for i, file in enumerate(self.files_in_dir[path]):
                if os.path.isdir(path + '/' + file):
                     self.see_dir(path + '/' + file)
            self.files_in_dir[path] = [x for x in self.files_in_dir[path] if os.path.isfile(path + '/' + x)]
            return True