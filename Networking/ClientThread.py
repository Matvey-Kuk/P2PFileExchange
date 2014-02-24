import threading


class ClientThread(threading.Thread):

    def __init__(self, ip, port, socket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.socket = socket
        print("[+] New thread started for "+ip+":"+str(port))

    def __run__(self):
        pass