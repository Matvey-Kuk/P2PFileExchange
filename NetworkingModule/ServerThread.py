import threading
import socket
import inspect

from NetworkingModule.Peer import *


class ServerThread(threading.Thread): #Класс для создания сокета, примающего соединения от других клиентов

    def __init__(self, host, port, peers):
        threading.Thread.__init__(self)

        self.host = host
        self.port = port
        self.peers = peers

        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Непосредственно создание сокета
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.tcp_socket.bind((self.host, self.port))    #Присваивание сокету указанного адреса и порта

    def run(self):
        while True:
            self.tcp_socket.listen(4) #Макс число клиентов ожидающих соединение
            (socket, (ip, port)) = self.tcp_socket.accept() #Возвращает кортеж с двумя элементами: новый сокет и адрес клиента
            peer = Peer(ip, port)
            peer.connect(socket)    #Подключение к новому сокету из кортежа, который получили раньше
            print("New incoming connection from " + ip + ":" + str(port))
            self.peers.append(peer)