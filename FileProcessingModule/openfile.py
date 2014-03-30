import pickle
from OpenDir import OpenDir
import os
import xml.etree.ElementTree as ET
from hashlib import md5
NAME_SYSTEM_FILE = 'system'


class FilesDifferences:
    def __init__(self, path):
        self.take_dir = OpenDir(path)
        self.main_dir = path
        #Создание вспомагательных дирректорий
        if not os.path.exists(self.main_dir + '/.' + NAME_SYSTEM_FILE):
            os.mkdir(self.main_dir + '/.' + NAME_SYSTEM_FILE)
            main = ET.Element('commit_file')
            cur_state = ET.SubElement(main, 'current_state')
            cur_state.text = "-1"
            ET.ElementTree(main).write(self.main_dir + '/.' + NAME_SYSTEM_FILE + "/comment.xml")
            hash_md5 = ET.Element('hash_file')
            ET.ElementTree(hash_md5).write(self.main_dir + '/.' + NAME_SYSTEM_FILE + "/hash.xml")
        self.state = self.take_state()

    def take_state(self):
        tree = ET.parse(self.main_dir + '/.' + NAME_SYSTEM_FILE + "/comment.xml")
        root = tree.getroot()
        return int(root.find('current_state').text)

    #Todo улучшить обработку фаила. Добавить количество комитов
    def change_state(self, move):
        tree = ET.parse(self.main_dir + '/.' + NAME_SYSTEM_FILE + "/comment.xml")
        root = tree.getroot()
        root.find('current_state').text = str(self.state + move)
        tree.write(self.main_dir + '/.' + NAME_SYSTEM_FILE + "/comment.xml")
        self.state += move

    def hash_file(self, path):
        tree = ET.parse(self.main_dir + '/.' + NAME_SYSTEM_FILE + "/hash.xml")
        root = tree.getroot()
        new_hash = md5(open(path, 'rb').read())
        hash_file = str(new_hash.hexdigest())
        sub = root.find(str("*[@name='" + path.split('/')[-1] + "']"))
        if sub.text == hash_file:
            return False
        else:
            sub.text = hash_file
            return True

    def max_state(self):
        tree = ET.parse(self.main_dir + '/.' + NAME_SYSTEM_FILE + "/comment.xml")
        root = tree.getroot()
        return len(root.findall('commit'))

    def create_hash_xml(self, files):
        tree = ET.parse(self.main_dir + '/.' + NAME_SYSTEM_FILE + "/hash.xml")
        root = tree.getroot()
        for keys in files:
            sub = root.find(str("[@name='" + keys + "']"))
            if sub:
                if not(sub.text == files[keys]):
                    sub.text = files[keys]
                    sub.set("changed", 'yes')
            else:
                file = ET.SubElement(root, 'file')
                file.set('name', keys)
                file.text = files[keys]
        tree.write(self.main_dir + '/.' + NAME_SYSTEM_FILE + "/hash.xml")

    def add_commit(self, commit):
        files = self.take_files()
        if files[0]:
            if self.state == self.max_state() - 1:
                self.change_state(1)
            len_lines = self.max_state()
            tree = ET.parse(self.main_dir + '/.' + NAME_SYSTEM_FILE + "/comment.xml")
            root = tree.getroot()
            sub = ET.SubElement(root, 'commit')
            sub.set('name', commit)
            sub.set('number', str(len_lines))
            for keys in files[0]:
                directory = ET.SubElement(sub, 'path_files')
                directory.set('path', keys)
                for items in files[0][keys]:
                    file = ET.SubElement(directory, 'file')
                    file.text = items
            if files[1]:
                self.create_hash_xml(files[1])
            tree.write(self.main_dir + '/.' + NAME_SYSTEM_FILE + "/comment.xml")
            return True
        else:
            return False

    def take_files(self):
        change_files = {}
        hash_files = {}
        for keys in self.take_dir.files_in_dir.keys():
            if not os.path.exists(self.main_dir + '/.' + NAME_SYSTEM_FILE + '/' + keys):
                os.makedirs(self.main_dir + '/.' + NAME_SYSTEM_FILE + '/' + keys)
            change_files[keys] = []
            for items in self.take_dir.files_in_dir[keys]:
                if os.path.exists(self.main_dir + '/.' + NAME_SYSTEM_FILE + '/' + keys + '/' + items):
                    if self.hash_file(keys + '/' + items):
                        delta = self.find_diff(keys + '/' + items,
                                               self.main_dir + '/.' + NAME_SYSTEM_FILE + '/' + keys + '/' + items + '/' +
                                               items)
                        change_files[keys].append(items)
                        self.save(self.main_dir + '/.' + NAME_SYSTEM_FILE + '/' + keys + '/' + items,
                                      delta, keys + '/' + items, items)
                else:
                    os.makedirs(self.main_dir + '/.' + NAME_SYSTEM_FILE + '/' + keys + '/' + items)
                    new_file = open(self.main_dir + '/.' + NAME_SYSTEM_FILE + '/' + keys + '/' + items + '/' + items,
                                    'wb')
                    old_file = open(keys + '/' + items, 'rb').read()
                    new_file.write(old_file)
                    new_hash = md5(old_file)
                    new_file.close()
                    change_files[keys].append(items)
                    hash_files[items] = new_hash.hexdigest()
            if len(change_files[keys]) == 0:
                del change_files[keys]
        return change_files, hash_files

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
        if self.state < self.max_state() - 1:
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
            tree = ET.parse(self.main_dir + '/.' + NAME_SYSTEM_FILE + "/comment.xml")
            root = tree.getroot()
            commit = root.findall('commit')
            for my_dir in commit[state]:
                parsing_str[my_dir.attrib['path']] = []
                for file in my_dir:
                    parsing_str[my_dir.attrib['path']].append(file.text)
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
test.back_step()
#test.forward_step()
