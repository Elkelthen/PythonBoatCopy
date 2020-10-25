from bluetooth import *

class BluetoothComms():
    
    def __init__(self):
            
        self.server_sock=BluetoothSocket( RFCOMM )
        self.server_sock.bind(("",PORT_ANY))
        self.server_sock.setblocking(0)
        self.server_sock.listen(1)
        self.client_sock, self.client_info = self.server_sock.accept()

    def read(self):
        try:
            data = self.client_sock.recv(1024).decode('utf-8')
            return data
        except IOError:
            pass
        
    def cleanup(self):
        self.client_sock.close()
        self.server_sock.close()

