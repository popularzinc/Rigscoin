import socket
import time
import ast

class Network:
    def __init__(self,IP='192.168.1.14',PORT=3000):
        self.SERVER_IP = IP
        self.PORT = PORT

    def SendTransaction(self,data):
        try:
            data.decode()
        except:
            data = str(data).encode()
        while True:
            try:
                s = socket.socket()
                s.connect((self.SERVER_IP,self.PORT))
                s.send(b'SENDTRANS')
                break
            except:
                return False
        # connect to server and send SENDTRANS
        time.sleep(1)
        a = 0
        b = 1024
        while data[a:b] != b'':
            s.send(data[a:b])
            a += 1024
            b += 1024
        s.send(b'EOF')
        s.close()
        return True

    def Ping(self):
        try:
            s = socket.socket()
            s.connect((self.SERVER_IP,self.PORT))
            return True
        except:
            return False

    def GetTransactions(self):
        while True:
            try:
                s = socket.socket()
                s.connect((self.SERVER_IP,self.PORT))
                s.send(b'GETTRANS')
                break
            except:
                pass

        end = b''
        data = s.recv(1024)
        end += data
        while data.decode()[-3:] != 'EOF':
            data = s.recv(1024)
            end += data
        if(end[-3:] == b'EOF'):
            end = end[:-3]
        transactions = []
        for i in end.decode().split('||||'):
            if(i.strip() != ''):
                transactions.append(ast.literal_eval(i))
        return(transactions)

    def GetNodes(self):
        while True:
            try:
                s = socket.socket()
                s.connect((self.SERVER_IP,self.PORT))
                s.send(b'LOG')
                return s.recv(1024).decode()
            except:
                pass
        end = b''
        data = s.recv(1024)
        end += data
        while data.decode()[-3:] != 'EOF':
            data = s.recv(1024)
            end += data
        if(end[-3:] == b'EOF'):
            end = end[:-3]
        return ast.literal_eval(end.decode())

    def BlockChainLength(self):
        while True:
            try:
                s = socket.socket()
                s.connect((self.SERVER_IP,self.PORT))
                s.send(b'BLOCKCHAIN_LEN')
                return s.recv(1024).decode()
            except:
                pass

    def CheckBlockChain(self,BCLength):
        while True:
            try:
                s = socket.socket()
                s.connect((self.SERVER_IP,self.PORT))
                s.send(b'BLOCKCHAIN_LEN')
                break
            except:
                pass

        L = int(s.recv(1024).decode())
        if(L > BCLength):
            return False
        else:
            return True

    def GetBlockChain(self):
        while True:
            try:
                s = socket.socket()
                s.connect((self.SERVER_IP,self.PORT))
                s.send(b'BLOCKCHAIN')
                break
            except:
                pass
        end = b''
        data = s.recv(1024)
        end += data
        while data.decode()[-3:] != 'EOF':
            data = s.recv(1024)
            end += data
        if(end[-3:] == b'EOF'):
            end = end[:-3]
        return ast.literal_eval(end.decode())

    def SendBlock(self,block):
        while True:
            try:
                data = str(block).encode()
                s = socket.socket()
                s.connect((self.SERVER_IP,int(self.PORT)))
                s.send(b'BLOCK')
                break
            except:
                time.sleep(5)
                continue
        time.sleep(1)
        a = 0
        b = 1024
        while data[a:b] != b'':
            s.send(data[a:b])
            a += 1024
            b += 1024
        s.send(b'EOF')
        s.close()
