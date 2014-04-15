from time import time


class Alteration(object):
    """Изменение для таблицы в базе данных."""

    def __init__(self, **kwargs):
        """
        Может создаваться по списку изменений и версии, а может создаваться из дампа с другого пира.
        """
        self.__rows = None
        self.__version = None

        if 'rows' in kwargs and 'version' in kwargs:
            self.__rows = kwargs['rows']
            self.__version = kwargs['version']
        elif 'dump' in kwargs:
            self.__init_from_dump(kwargs['dump'])

        self.__creation_time = time()

    def get_rows(self):
        return self.__rows.copy()

    def get_creation_time(self):
        return self.__creation_time

    def get_version(self):
        return self.__version

    def __init_from_dump(self, dump):
        self.__version = None
        self.__rows = None
        raise Exception('Method is not written yet')
