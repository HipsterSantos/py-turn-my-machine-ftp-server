const net = require('net');
const fs = require('fs');
const path = require('path');

class FTPServer {
  constructor(host = '0.0.0.0', port = 21, rootDir = process.cwd()) {
    this.host = host;
    this.port = port;
    this.rootDir = rootDir;
  }

  start() {
    const server = net.createServer((socket) => this.handleClient(socket));

    server.listen(this.port, this.host, () => {
      console.log(`FTP server started on ${this.host}:${this.port}`);
    });

    server.on('error', (err) => {
      console.error(`Server error: ${err.message}`);
    });
  }

  handleClient(socket) {
    console.log(`Connection from ${socket.remoteAddress}:${socket.remotePort}`);
    socket.write('220 Welcome to the custom FTP server\r\n');
    let currentDir = this.rootDir;

    socket.on('data', (data) => {
      const command = data.toString().trim();
      console.log(`Command received: ${command}`);

      if (command.startsWith('USER')) {
        socket.write('331 User name okay, need password\r\n');
      } else if (command.startsWith('PASS')) {
        socket.write('230 User logged in, proceed\r\n');
      } else if (command.startsWith('PWD')) {
        socket.write(`257 "${currentDir}" is the current directory\r\n`);
      } else if (command.startsWith('LIST')) {
        fs.readdir(currentDir, (err, files) => {
          if (err) {
            socket.write('450 Requested file action not taken\r\n');
          } else {
            socket.write('150 Here comes the directory listing\r\n');
            socket.write(files.join('\r\n') + '\r\n');
            socket.write('226 Directory send okay\r\n');
          }
        });
      } else if (command.startsWith('QUIT')) {
        socket.write('221 Goodbye\r\n');
        socket.end();
      } else {
        socket.write('502 Command not implemented\r\n');
      }
    });

    socket.on('error', (err) => {
      console.error(`Socket error: ${err.message}`);
    });

    socket.on('close', () => {
      console.log(`Connection closed: ${socket.remoteAddress}:${socket.remotePort}`);
    });
  }
}

// Start the server
const ftpServer = new FTPServer('127.0.0.1', 21);
ftpServer.start();
