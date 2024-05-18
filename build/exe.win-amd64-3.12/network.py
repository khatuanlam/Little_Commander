import pickle
import socket


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server = "localhost"
        self.port = 5555
        self.address = (self.server, self.port)
        self.post = self.connect()

    def getPost(self):
        return self.post

    def connect(self):
        try:
            self.client.connect(self.address)
            print("Server Connected")
            return self.client.recv(4094 * 2).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            # print("DA GUI SEND")
            pick = pickle.loads(self.client.recv(2048 * 2))
            # print("DA NHAN SEND")
            return pick
        except socket.error as e:
            print("NETWORK Error")
            print(e)
