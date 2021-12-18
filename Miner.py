import sys
sys.path.append('../')
import Rigs
import time
import ast
import socket
import time

BlockLength = 1

SERVER_IP = '192.168.1.14'
PORT = 3000
ADDR = '4f81a5e6baa28bc73fe21fd6cd085ed886392934155c19dea430c2266d3bee65'

def GetTransactions():
    try:
        s = socket.socket()
        s.connect((SERVER_IP,int(PORT)))
        s.send(b'GETTRANS')
    except:
        return []

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

def CheckBlockChain():
    try:
        s = socket.socket()
        s.connect((SERVER_IP,int(PORT)))
        s.send(b'BLOCKCHAIN')
    except:
        return

    L = int(s.recv(1024).decode())
    bc = Rigs.BlockChain()
    data = bc.Load()
    if(L > len(data)):
        print('[*] Found Larger BlockChain')
        s.send(b'CONTINUE')
        end = b''
        data = s.recv(1024)
        end += data
        while data.decode()[-3:] != 'EOF':
            data = s.recv(1024)
            end += data
        if(end[-3:] == b'EOF'):
            end = end[:-3]
        bc.blockchain = ast.literal_eval(end.decode())
        if(bc.Verify()):
            bc.SaveWhole()
            print('[+] New BlockChain Saved')
        else:
            print('[-] New BlockChain Invalid. Discarded')
    else:
        s.send(b' ')

def SendBlock(block):
    while True:
        try:
            data = str(block).encode()
            s = socket.socket()
            s.connect((SERVER_IP,int(PORT)))
            s.send(b'BLOCK')
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
        break

def Add(transactions,get):
    res = []
    for i in transactions:
        if i not in res:
            res.append(i)
    for i in get:
        if i not in res:
            res.append(i)
    return res

def main():
    transactions = []
    while True:
        if(len(transactions) >= BlockLength):
            print('[*] Got Enough Transactions for a Block')
            bc = Rigs.BlockChain().Load()
            try:
                block = Rigs.Block(bc[-1]['hash'])
            except:
                block = Rigs.Block('0'*64)
            for i in transactions:
                block.AddRawTransaction(i)
            MinedBlock = block.Mine(ADDR)
            if(MinedBlock == True):
                print('[+] Block Mined')
                bc = Rigs.BlockChain()
                bc.AddBlock(block)
                bc.Save()
                SendBlock(block.Build())
                print('[+] Block Sent To Network')
                transactions = []
            else:
                print('[-] Block Invalid: '+str(MinedBlock))
        time.sleep(5)
        transactions = Add(transactions,GetTransactions())
        time.sleep(5)
        CheckBlockChain()


main()
