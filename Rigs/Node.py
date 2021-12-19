import socket
import ast
import Rigs
from threading import Thread

class Node:
    def __init__(self,port=3000):
        self.port = port
        self.log = []
        self.transactions = []
        self.take = []

    def CleanTransactions(self):
        re = []
        n = 0
        for i in self.transactions:
            if(i not in re):
                re.append(i)
        self.transactions = re

    def Log(self,ip):
        if(ip not in self.log):
            self.log.append(ip)

    def Main(self):
        blocks = []
        while True:
            #import time
            #print('wait...')
            #time.sleep(5)
            #self.transactions.append('fdsf')
            #time.sleep(999)
            s = socket.socket()
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('0.0.0.0',int(self.port)))
            s.listen(1)
            s,a = s.accept()
            self.Log(a[0])
            #print('[*] '+str(a[0])+' Connected.')
            re = s.recv(1024).decode()
            if(re == 'SENDTRANS'):
                print('[*] '+str(a[0])+' Sending Transaction')
                end = b''
                data = s.recv(1024)
                end += data
                while data.decode()[-3:] != 'EOF':
                    data = s.recv(1024)
                    end += data
                if(end[-3:] == b'EOF'):
                    end = end[:-3]
                transaction = ast.literal_eval(end.decode())
                V = Rigs.VerifyTransaction(transaction)
                if(V == True):
                    self.transactions.append(transaction)
                    self.CleanTransactions()
                    self.take.append(transaction)
                    print(self.transactions)
                    print('[+] Valid Transaction Received')
                else:
                    print(V)

            elif(re == 'LOG'):
                data = str(self.log).encode()
                a = 0
                b = 1024
                while data[a:b] != b'':
                    s.send(data[a:b])
                    a += 1024
                    b += 1024
                s.send(b'EOF')
                s.close()

            elif(re == 'BLOCK'):
                print('[*] '+str(a[0])+' Sending Block')
                end = b''
                data = s.recv(1024)
                end += data
                while data.decode()[-3:] != 'EOF':
                    data = s.recv(1024)
                    end += data
                if(end[-3:] == b'EOF'):
                    end = end[:-3]
                block = ast.literal_eval(end.decode())
                new_block = Rigs.Block()
                new_block.Load(block)
                print('[*] Received Block')
                if(new_block.Verify()):
                    #self.transactions.append(block['transactions'])
                    #self.CleanTransactions()
                    bc = Rigs.BlockChain()
                    bc.Load()
                    bc.AddBlock(new_block)
                    print('[*] Validating New BlockChain')
                    V = bc.VerifyBlockChain()
                    if(V == True):
                        bc.OverwriteSave()
                        print('[+] Block Valid and added to BlockChain')
                    else:
                        print('[-] BlockChain invalid: '+V)

                else:
                    print('[+] Block Invalid')

            elif(re == 'GETTRANS'):
                for transaction in self.transactions:
                    data = str(transaction).encode()
                    a = 0
                    b = 1024
                    while data[a:b] != b'':
                        s.send(data[a:b])
                        a += 1024
                        b += 1024
                    s.send(b'||||')
                s.send(b'EOF')
                s.close()

            elif(re == 'BLOCKCHAIN_LEN'):
                bc = Rigs.BlockChain()
                data = bc.Load()
                s.send(str(len(data)).encode())

            elif(re == 'BLOCKCHAIN'):
                bc = Rigs.BlockChain()
                data = bc.Load()
                data = str(data).encode()
                a = 0
                b = 1024
                while data[a:b] != b'':
                    s.send(data[a:b])
                    a += 1024
                    b += 1024
                s.send(b'EOF')
                s.close()

    def Start(self):
        t = Thread(target=self.Main)
        t.start()
