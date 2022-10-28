import socket

from config import TELE_UDP_BUFFER_SIZE


class UdpPort:
    def __init__(self, listen_ip: str, listen_port: int):
        self.listen_ip = listen_ip
        self.listen_port = listen_port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.listen_ip, self.listen_port))

    def receive(self) -> (bytes, (str, int)):
        return self.socket.recvfrom(TELE_UDP_BUFFER_SIZE)

    def send(self, data: bytes, ip: str, port: int):
        self.socket.sendto(data, (ip, port))

    def close(self):
        self.socket.close()
