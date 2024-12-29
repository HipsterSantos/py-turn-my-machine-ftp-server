from src.ftp_server import FTPServer

class CustomFTPServer(FTPServer):
    def handle_client(self, client_socket):
        client_socket.sendall(b"220 Welcome to the Custom FTP Server\r\n")
        while True:
            data = client_socket.recv(1024).decode().strip()
            if not data:
                break

            if data.startswith("USER"):
                client_socket.sendall(b"331 Custom User Name Accepted\r\n")
            else:
                client_socket.sendall(b"502 Command not implemented in Custom Server\r\n")

server = CustomFTPServer(host='127.0.0.1', port=2121)
server.start()