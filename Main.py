from Networking import Networking


class Main(object):
    """Это основной класс, через который запускается приложение."""

    def __init__(self):
        networking = Networking.Networking("0.0.0.0", 1234)

main = Main()