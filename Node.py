import socket
import ast
import Rigs
from threading import Thread

class Node:
    def __init__(self,port=3000):
        self.port = port
        self.log = []

    def RemoveTransactions(self,transactions,block_transactions):
        re = []
        n = 0
        for i in transactions:
            if(i['tx_hash'] not in str(block_transactions[n])):
                re.append(i)
            n += 1
        return re

    def Log(self,ip):
        if(ip not in self.log):
            self.log.append(ip)

    def Main(self):
        transactions = []
        blocks = []
        while True:
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
                if(V):
                    transactions.append(transaction)
                    RemoveTransactions(transactions,transaction)
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
                    transactions = RemoveTransactions(transactions,block['transactions'])
                    bc = Rigs.BlockChain()
                    bc.Load()
                    bc.AddBlock(new_block)
                    print('[*] Validating New BlockChain')
                    V = bc.VerifyBlockChain()
                    if(V):
                        bc.OverwriteSave()
                    else:
                        print('[-] BlockChain invalid: '+V)
                    print('[+] Block Valid and added to BlockChain')
                else:
                    print('[+] Block Invalid')

            elif(re == 'GETTRANS'):
                for transaction in transactions:
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
