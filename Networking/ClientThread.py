import threading


class ClientThread(threading.Thread):

    def __init__(self, ip, port, socket, data_received_callback, disconnected_callback):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.socket = socket
        self.data_received_callback = data_received_callback
        self.disconnected_callback = disconnected_callback
        print("[+] New thread started for "+ip+":"+str(port))

    def run(self):
        print("client loop started")
        while True:
            data = self.socket.recv(1024)
            print('Received', repr(data))