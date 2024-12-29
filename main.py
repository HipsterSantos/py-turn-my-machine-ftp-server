import socket
import threading

class FTPServer: 
    def __init__(self,host='0.0.0.0',port=21):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    def start(self):
        self.server_socket.bidn( (self.host,self.port))
        self.server_socket.listen(5)
        print(f"FTP server started on {self.host}:{self.port}")
        while True:
            client_socket,client_address = self.server_socket.accept()
            print(f"Connection from {client_address}")
            threading.Thread(target=self.handle_client,args=(client_socket,)).start()

    def handle_client(self,client_socket):            
        client_socket.sendall(b"220 Welcome to the custom FTP server\r\n")
        while True:
            data = client_socket.recv(1024).decode().strip()
            if not data:
                break
            print(f"Command received: {data}")
            
            # Handle specific commands
            if data.startswith("USER"):
                client_socket.sendall(b"331 User name okay, need password\r\n")
            elif data.startswith("PASS"):
                client_socket.sendall(b"230 User logged in, proceed\r\n")
            elif data.startswith("QUIT"):
                client_socket.sendall(b"221 Goodbye\r\n")
                client_socket.close()
                break
            else:
                client_socket.sendall(b"502 Command not implemented\r\n")

# Run the FTP server
ftp_server = FTPServer()
ftp_server.start()
     