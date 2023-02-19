import socket
import threading

class ProxyServer:
    def __init__(self, host='0.0.0.0', port=8000):
        self.host = host
        self.port = port
        self.clients = []
        self.previous_proxy = None

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen()

        while True:
            client_socket, address = self.socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, address))
            client_thread.start()

    def handle_client(self, client_socket, address):
        self.clients.append(client_socket)
        print(f'New client connected: {address}')

        while True:
            try:
                message = client_socket.recv(4096)
                if not message:
                    self.clients.remove(client_socket)
                    print(f'Client disconnected: {address}')
                    break
                if self.previous_proxy is not None and client_socket != self.previous_proxy:
                    self.previous_proxy.sendall(message)
                for c in self.clients:
                    if c != client_socket and c != self.previous_proxy:
                        c.sendall(message)
            except ConnectionError:
                self.clients.remove(client_socket)
                print(f'Client disconnected: {address}')
                break

    def set_previous_proxy(self, previous_proxy):
        self.previous_proxy = previous_proxy

if __name__ == '__main__':
    proxy_server = ProxyServer()
    proxy_server.start()
