import os
#На вход подается словарем , где ключ это путь до фаила , а объект это название фаила


class ControlAccess:
    def __init__(self, path):
        self.system_path = path

    #Todo По идее можно по красивее реализовать
    def operation_on_files(self, func, mode):
        for keys in self.system_path:
            for items in self.system_path[keys]:
                func(keys + items, mode)

    def limit_records(self):
        self.operation_on_files(os.chmod, 0o444)

    def include_all_right(self):
        self.operation_on_files(os.chmod, 0o777)