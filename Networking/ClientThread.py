import threading


class ClientThread(threading.Thread):

    def __init__(self, socket, data_received_callback, disconnected_callback):
        threading.Thread.__init__(self)
        self.socket = socket
        self.data_received_callback = data_received_callback
        self.disconnected_callback = disconnected_callback
        print("[+] New thread started for connection")

    def run(self):
        print("client loop started")
        while True:
            data = self.socket.recv(1024)
            print(type(data))
            print('Received', repr(data))