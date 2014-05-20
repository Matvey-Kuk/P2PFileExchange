import threading


class ClientThread(threading.Thread):

    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.socket = socket
        socket.setblocking(0)

    def run(self):
        raise NotImplementedError("Эту функцию необходимо унаследовать")