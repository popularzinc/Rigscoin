import socket
import Rigs
import ast

PORT = 3000

def RemoveTransactions(transactions,block_transactions):
    n = 0
    re = []
    for i in transactions:
        if(i['tx_hash'] not in str(block_transactions[n])):
            re.append(i)
        n+=1
    return re

def Main():
    transactions = []
    blocks = []
    while True:
        print(len(transactions))
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0',int(PORT)))
        s.listen(1)
        s,a = s.accept()
        print('[*] '+str(a[0])+' Connected.')
        re = s.recv(1024).decode()
        if(re == 'SENDTRANS'):
            end = b''
            data = s.recv(1024)
            end += data
            while data.decode()[-3:] != 'EOF':
                data = s.recv(1024)
                end += data
            if(end[-3:] == b'EOF'):
                end = end[:-3]
            transaction = ast.literal_eval(end.decode())
            bc = Rigs.BlockChain()
            if(bc.VerifyTransaction(transaction)):
                transactions.append(transaction)

        elif(re == 'BLOCK'):
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
                V = bc.Verify()
                if(V):
                    bc.SaveWhole()
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

        elif(re == 'BLOCKCHAIN'):
            bc = Rigs.BlockChain()
            data = bc.Load()
            s.send(str(len(data)).encode())
            if(s.recv(1024).decode() == 'CONTINUE'):
                data = str(data).encode()
                a = 0
                b = 1024
                while data[a:b] != b'':
                    s.send(data[a:b])
                    a += 1024
                    b += 1024
                s.send(b'EOF')
            s.close()

Main()
