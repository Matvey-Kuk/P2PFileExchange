

class VersionsRange(object):
    """
    Это буквально "Диапазон версий". Нужен для тех случаев, когда в "шарик" смержены несколько шариков разных версий.
    Имеет операторы сравнения итд.
    """

    def __init__(self, **kwargs):
        self.__first_version = None
        self.__last_version = None
        if 'version' in kwargs:
            self.__first_version = kwargs['version']
            self.__last_version = kwargs['version']
        elif 'first' in kwargs and 'last' in kwargs:
            self.__first_version = kwargs['first']
            self.__last_version = kwargs['last']
        else:
            raise Exception('Init failed.')
        if not self.__last_version is None:
            if self.__first_version > self.__last_version:
                raise Exception('Init failed.')

    def is_version_in_range(self, version):
        if self.__last_version is None:
            return version >= self.__first_version
        else:
            return self.__last_version >= version >= self.__first_version

    def get_first_version(self):
        return self.__first_version

    def get_last_version(self):
        return self.__last_version

    def includes(self, versions_range):
        """
        Проверяет, входит ли указанный диапазон в рамки текущего.
        """
        if self.__last_version is None:
            return self.__first_version <= versions_range.get_first_version()
        else:
            return self.__last_version >= versions_range.get_last_version() and \
                self.__first_version <= versions_range.get_first_version()

    def __eq__(self, other):
        """
        Перегрузим оператор эквивалентности
        """
        return self.__first_version == other.get_first_version() and self.__last_version == other.get_last_version()

    def __lt__(self, other):
        """
        self < other оператор
        """
        if self.__last_version is None:
            return False
        else:
            return self.get_last_version() < other.get_first_version()

    def __gt__(self, other):
        """
        self > other оператор
        """
        return other.get_last_version() < self.get_first_version()

    def __repr__(self):
        return 'First: ' + str(self.__first_version) + ' Last: ' + str(self.__last_version)

    @staticmethod
    def merge(versions_ranges):
        first = None
        last = None
        last_infinity = False

        for version_range in versions_ranges:
            if (first is None) or (first > version_range.get_first_version()):
                first = version_range.get_first_version()
            if version_range.get_last_version() is None:
                last_infinity = True
                last = None
            if (last is None or last < version_range.get_last_version()) and not last_infinity:
                last = version_range.get_last_version()

        return VersionsRange(first=first, last=last)