import pickle
from OpenDir import OpenDir
import os
NAME_SYSTEM_FILE = 'system'


class FilesDifferences:
    def __init__(self, path):
        self.take_dir = OpenDir(path)
        self.main_dir = path
        #Создание вспомагательных дирректорий
        if not os.path.exists(self.main_dir + '/.' + NAME_SYSTEM_FILE):
            os.mkdir(self.main_dir + '/.' + NAME_SYSTEM_FILE)
            open(self.main_dir + '/.' + NAME_SYSTEM_FILE + '/' + 'commit.txt', 'w').write(str(-1))
        self.state = self.take_state()

    def take_state(self):
        if os.path.exists(self.main_dir + '/.' + NAME_SYSTEM_FILE + '/' + 'commit.txt'):
            text = [x for x in open(self.main_dir + '/.' + NAME_SYSTEM_FILE + '/' + 'commit.txt').readline()]
            number = ''
            for sym in text:
                number += sym
            return int(number)
        else:
            return -1

    #Todo улучшить обработку фаила
    def change_state(self, move):
            commit_file = open(self.main_dir + '/.' + NAME_SYSTEM_FILE + '/' + 'commit.txt', 'r').read()
            lines_commit_file = commit_file.split('\n')
            try:
                lines_commit_file.remove('')
            except:
                pass
            lines_commit_file[0] = str(self.state + move)
            commit_file = open(self.main_dir + '/.' + NAME_SYSTEM_FILE + '/' + 'commit.txt', 'w')
            for lines in lines_commit_file:
                commit_file.write(lines + '\n')
            commit_file.flush()
            return len(lines_commit_file) - 1

    def max_state(self):
        commit_file = open(self.main_dir + '/.' + NAME_SYSTEM_FILE + '/' + 'commit.txt', 'r').read()
        lines_commit_file = commit_file.split('\n')
        lines_commit_file.remove('')
        return len(lines_commit_file) - 2

    #Todo Возможна ошибка парсинга из за слешей в комите
    def add_commit(self, commit):
        if not(commit.find('/') or commit.find('|') or commit.find('\\')):
            return "Строка комита не должна содержать /, | ,\\"
        files = self.take_files()
        if not (files == {}):
            len_lines = self.change_state(1)
            modify_test = ''
            for keys in files:
                modify_test += '|' + keys + '\\'
                for items in files[keys]:
                    modify_test += items + '/'
            str_commit = str(len_lines) + '"' + commit + '"' + modify_test
            commit_file = open(self.main_dir + '/.' + NAME_SYSTEM_FILE + '/' + 'commit.txt', 'a')
            commit_file.write(str_commit)
            commit_file.flush()
            return True
        else:
            return "Нет измененных фаилов"

    def take_files(self):
        change_files = {}
        for keys in self.take_dir.files_in_dir.keys():
            if not os.path.exists(self.main_dir + '/.' + NAME_SYSTEM_FILE + '/' + keys):
                os.makedirs(self.main_dir + '/.' + NAME_SYSTEM_FILE + '/' + keys)
            change_files[keys] = []
            for items in self.take_dir.files_in_dir[keys]:
                if os.path.exists(self.main_dir + '/.' + NAME_SYSTEM_FILE + '/' + keys + '/' + items):
                    delta = self.find_diff(keys + '/' + items,
                                           self.main_dir + '/.' + NAME_SYSTEM_FILE + '/' + keys + '/' + items + '/' +
                                           items)
                    if len(delta) > 0:
                        pass
                        change_files[keys].append(items)
                        self.save(self.main_dir + '/.' + NAME_SYSTEM_FILE + '/' + keys + '/' + items,
                                  delta, keys + '/' + items, items)
                else:
                    os.makedirs(self.main_dir + '/.' + NAME_SYSTEM_FILE + '/' + keys + '/' + items)
                    new_file = open(self.main_dir + '/.' + NAME_SYSTEM_FILE + '/' + keys + '/' + items + '/' + items,
                                    'wb')
                    new_file.write(open(keys + '/' + items, 'rb').read())
                    new_file.close()
                    change_files[keys].append(items)
            if len(change_files[keys]) == 0:
                del change_files[keys]
        return change_files

    @staticmethod
    def find_diff(path_file, path_store_file):
        file = open(path_file, 'rb').read()
        old_file = open(path_store_file, 'rb').read()
        delta = {}
        pos = -1
        for oldRead, Read in zip(old_file, enumerate(file)):
            if Read[1] != oldRead:
                if pos < 0:
                    pos = Read[0]
                    delta[pos] = [Read[1] - oldRead]
                else:
                    delta[pos].append(Read[1] - oldRead)
            else:
                pos = -1
        if len(old_file) > len(file):
            delta[len(file)] = old_file[len(file): len(old_file)]
        if len(old_file) < len(file):
            delta[len(old_file)] = file[len(old_file): len(file)]
        return delta

    def save(self, path, delta, path_new_file, path_old_file):
        delta_file = open(path + '/_delta' + str(self.state), 'wb')
        pickle.dump(delta, delta_file)
        delta_file.close()
        new_file = open(path_new_file, 'rb').read()
        open(path + '/' + path_old_file, 'wb').write(new_file)

    def back_step(self):
        if self.state > 0:
            self.step(-1)
            return True
        else:
            return False

    def forward_step(self):
        if self.state < self.max_state():
            self.step(1)
            return True
        else:
            return False

    def step(self, move):
        if move == -1:
            change_files = self.take_change_files(self.state)
        else:
            change_files = self.take_change_files(self.state + move)
        self.change_state(move)
        for keys in change_files.keys():
            for items in change_files[keys]:
                if os.path.exists(self.main_dir + '/.' + NAME_SYSTEM_FILE + '/' + keys + '/' + items + '/_delta' +
                                  str(self.state)):
                    self.remark(keys + '/' + items,
                                self.main_dir + '/.' + NAME_SYSTEM_FILE + '/' + keys + '/' + items + '/_delta' +
                                str(self.state), move)

    def take_change_files(self, state):
        # словарь, хранящий измененые объекты указанного комита
        parsing_str = {}
        if state >= 0:
            check_cur_state = -1
            for commit_file in open(self.main_dir + '/.' + NAME_SYSTEM_FILE + '/' + 'commit.txt', 'r'):
                if check_cur_state == state:
                    break
                else:
                    check_cur_state +=1
            commit_file = commit_file.split('|')[1:]
            for path_commit in commit_file:
                path = path_commit.split('\\')
                parsing_str[path[0]] = path[1].split('/')[0:-1]
            return parsing_str
        else:
            return None

    @staticmethod
    def remark(path, path_delta, move):
        open_file = open(path_delta, 'rb')
        delta = pickle.load(open_file)
        remake_file = list(open(path, 'rb').read())
        for keys in delta:
            for items in enumerate(delta[keys]):
                if keys + items[0] < len(remake_file):
                    if remake_file[keys + items[0]] == move*items[1]:
                        remake_file[keys + items[0]] = 0
                    else:
                        remake_file[keys + items[0]] += move*items[1]
                else:
                    remake_file.append(items[1])
        new_text = open(path, 'r+')
        for sym in remake_file:
            if not(sym == 0):
                new_text.write(chr(sym))
            else:
                new_text.truncate()
                break
        new_text.flush()

test = FilesDifferences('base')
#test.add_commit("The first step")
#test.back_step()
#test.forward_step()
