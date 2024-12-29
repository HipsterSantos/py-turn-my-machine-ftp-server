from src.ftp_server import FTPServer

server = FTPServer(host='127.0.0.1', port=2121)
server.start()