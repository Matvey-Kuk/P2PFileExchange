

class Alteration(object):
    """
    Изменение- единица, которой оперирует база данных. Тот самый "шарик".
    """

    def __init__(self):
        self.changes = {}
        self.version = None
        self.creation_time = None