import bluetooth

galaxy = "F8:E6:1A:43:6E:39"
port = 1

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((galaxy, port))
        
while True:
        print(sock.recv(2048))