

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
        elif 'dump' in kwargs:
            self.__first_version = kwargs['dump']['first']
            self.__last_version = kwargs['dump']['last']
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

    def concretize_infinity(self, concrete_last_version):
        if self.__last_version is None:
            self.__last_version = int(concrete_last_version)

    def get_first(self):
        return self.__first_version

    def get_last(self):
        return self.__last_version

    def includes(self, versions_range):
        """
        Проверяет, входит ли указанный диапазон в рамки текущего.
        """
        if self.__last_version is None:
            return self.__first_version <= versions_range.get_first()
        else:
            return self.__last_version >= versions_range.get_last() and \
                self.__first_version <= versions_range.get_first()

    def __eq__(self, other):
        """
        Перегрузим оператор эквивалентности
        """
        if type(other) is VersionsRange:
            return self.__first_version == other.get_first() and self.__last_version == other.get_last()
        else:
            return False

    def __lt__(self, other):
        """
        self < other оператор
        """
        if self.__last_version is None:
            return False
        else:
            return self.get_last() < other.get_first()

    def __gt__(self, other):
        """
        self > other оператор
        """
        return other.get_last() < self.get_first()

    def __repr__(self):
        return 'First: ' + str(self.__first_version) + ' Last: ' + str(self.__last_version)

    def get_dump(self):
        return {
            'first': self.__first_version,
            'last': self.__last_version
        }

    def get_size(self):
        return self.__last_version - self.__first_version + 1

    @staticmethod
    def divide_range(versions_range):
        """
        Разделить диапазон на 2.
        """
        if versions_range.get_size() > 1:
            result = [
                VersionsRange(
                    first=versions_range.get_first(),
                    last=versions_range.get_first() + round(versions_range.get_size() / 2) - 1
                ),
                VersionsRange(
                    first=versions_range.get_first() + round(versions_range.get_size() / 2),
                    last=versions_range.get_last()
                )
            ]
        else:
            result = [versions_range]
        return result

    @staticmethod
    def subtraction(minuend, subtrahend):
        """
        Вычитание некого диапазона из текущего
        """
        result = []
        if not minuend.get_first() >= subtrahend.get_first():
            result.append(
                VersionsRange(first=minuend.get_first(), last=subtrahend.get_first() - 1)
            )
        if not minuend.get_last() <= subtrahend.get_last():
            result.append(
                VersionsRange(first=subtrahend.get_last() + 1, last=minuend.get_last())
            )
        return result

    @staticmethod
    def merge(versions_ranges):
        first = None
        last = None
        last_infinity = False

        for version_range in versions_ranges:
            if (first is None) or (first > version_range.get_first()):
                first = version_range.get_first()
            if version_range.get_last() is None:
                last_infinity = True
                last = None
            if (last is None or last < version_range.get_last()) and not last_infinity:
                last = version_range.get_last()

        return VersionsRange(first=first, last=last)