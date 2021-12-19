import sys
sys.path.append('../')
import Rigs
from Rigs import Network
from Rigs import Node
import time
import ast
import socket
import time

BlockLength = 1

RECV_ADDR = '7ZAJEBDFLr8FYmBqKA8G5L2MMeRiJKPHQJTiircmuRoS'


#def SendTransaction(data):
#def Ping():
#def GetTransactions():
#def BlockChainLength():
#def CheckBlockChain(BCLength):
#def GetBlockChain():
#def SendBlock(block):

Network = Network.Network()
Node = Node.Node()
Node.Start()

def CheckBlockChain():
    bc = Rigs.BlockChain()
    data = bc.Load()
    if(Network.CheckBlockChain(len(data)) == False):
        print('[*] Found Larger BlockChain')
        bc.blockchain = Network.GetBlockChain()
        if(bc.VerifyBlockChain()):
            print('[+] New BlockChain Saved')
            bc.OverwriteSave()
        else:
            print('[-] New BlockChain Invalid. Discarded')

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
        #transactions = Add(transactions,Node.take)
        #Node.take = []
        print(transactions)
        if(len(transactions) >= BlockLength):
            print('[*] Got Enough Transactions for a Block')
            bc = Rigs.BlockChain().Load()
            try:
                block = Rigs.Block(bc[-1]['hash'])
            except:
                block = Rigs.Block('0'*64)
            for i in transactions:
                block.AddRawTransaction(i)
            MinedBlock = block.Mine(RECV_ADDR)
            if(MinedBlock == True):
                print('[+] Block Mined')
                bc = Rigs.BlockChain()
                bc.AddBlock(block)
                bc.Save()
                Network.SendBlock(block.Build())
                print('[*] Block Sent To Network')
                print('[+] '+str(block.REWARD)+' Coins Earned')
                transactions = []
            else:
                print(block.transactions)
                print('[-] Block Invalid: '+str(MinedBlock))
        time.sleep(5)
        transactions = Add(transactions,Network.GetTransactions())
        time.sleep(5)
        CheckBlockChain()


main()
