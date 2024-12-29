import unittest
from src.ftp_server import FTPServer

class TestFTPServer(unittest.TestCase):
    def test_initialization(self):
        server = FTPServer(host='127.0.0.1', port=2121)
        self.assertEqual(server.host, '127.0.0.1')
        self.assertEqual(server.port, 2121)

if __name__ == '__main__':
    unittest.main()