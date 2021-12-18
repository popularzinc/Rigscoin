import hashlib
import ast
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
import base64
from Crypto.Hash import SHA256
import time
import os
import socket
import random

SERVER_IP = '192.168.1.14'
PORT = 3000

class BlockChain:
    def __init__(self):
        self.blockchain = []

    def AddBlock(self,block):
        self.blockchain.append(block.Build())

    def AddRawBlock(self,block):
        self.blockchain.append(block)

    def Save(self):
        data = self.Load()+self.blockchain
        f = open('blockchain','w')
        f.write(str(data))
        f.close()

    def SaveWhole(self):
        data = self.blockchain
        f = open('blockchain','w')
        f.write(str(data))
        f.close()

    def Load(self):
        try:
            f = open('blockchain','r')
            data = f.read()
            f.close()
        except:
            return []
        try:
            self.blockchain = ast.literal_eval(data)
            return ast.literal_eval(data)
        except:
            return []

    def Verify(self):
        all = []
        n = 0
        for block in self.blockchain[1:]:
            if(not self.VerifyBlock(block['transactions'])):
                return 'Block '+str(n)+' Invalid'
            for transaction in block['transactions']:
                all.append(transaction['tx_hash'])
            n += 1
        for i in all:
            if(all.count(i) > 1):
                return 'Transaction: '+str(i)+' Repeats | Fraudulant Transaction'
        return True

    def VerifyBlock(self,transactions):
        for transaction in transactions:
            if(transaction == transactions[-1]):
                continue
            if(not self.VerifyTransaction(transaction)):
                return 'Invalid Signature'
            key = Key()
            if(float(key.Balance(transaction['sender']))-float(transaction['ammount']) < 0.0):
                return 'Not Enough Funds'
        return True

    def VerifyTransaction(self,transaction):
        public_key = transaction['public_key']
        sig = transaction['signature']
        data = Hash(str(transaction['sender'])+str(transaction['recv'])+str(transaction['ammount'])+str(transaction['time']))
        return Verify(public_key,sig,data)

class Block:
    def __init__(self,lbhash=''):
        self.transactions = []
        self.lbhash = lbhash
        self.GoalTime = 60*1
        self.deviation = 30
        self.hash = ''
        self.nonce = 0
        self.build = ''
        self.lowest = 4
        self.difficulty = 4
        self.fee = 0.005
        self.reward = 20.0

    def AddTransaction(self,transaction):
        self.transactions.append(transaction.Build())

    def AddRawTransaction(self,transaction):
        self.transactions.append(transaction)

    def Load(self,data):
        self.transactions = data['transactions']
        self.lbhash = data['previous_hash']
        self.GoalTime = 60*1
        self.deviation = 30
        self.hash = data['hash']
        self.nonce = data['nonce']
        self.build = {'hash':data['hash'],'time':data['time'],'nonce':data['nonce'],'previous_hash':data['previous_hash'],'transactions':data['transactions'],'fee':data['fee']}
        self.lowest = 4
        self.difficulty = 4

    def GetDifficulty(self):
        return 4
        bc = BlockChain().Load()
        if(len(bc) == 0):
            return
        #for block in bc:
        block = bc[-1]
        lbt = block['transactions'][-1]['time']
        print(str(int(float(block['time'])-float(lbt)) - self.GoalTime))
        print(str(int(float(block['time'])-float(lbt))), str(self.GoalTime))
        if(int(float(block['time'])-float(lbt)) - self.GoalTime in range(-self.deviation,self.deviation)):
            pass
        elif int(float(block['time'])-float(lbt)) > self.GoalTime:
            self.difficulty -= 1
        else:
            self.difficulty += 1
        if(self.difficulty < self.lowest):
            self.difficulty = self.lowest
        print(self.difficulty)

    def Mine(self,MINER_ADDR):
        if(self.lbhash == 'GENYSIS'):
            self.lbhash = '0'*64
        else:
            verify = self.Verify()
            if(verify != True):
                return verify
            self.GetDifficulty()
        block_fee_ammount = 0.0
        REWARD = block_fee_ammount+self.reward
        self.transactions += [Transaction('REWARD',MINER_ADDR,REWARD,'REWARD').Build()]

        for transaction in self.transactions:
            if(transaction['sender'] == 'REWARD'):
                transaction['fee'] = '0'
                continue
            transaction['fee'] = str(float(transaction['ammount'])*float(self.fee))
            block_fee_ammount += float(transaction['ammount'])*float(self.fee)

        hash = (Hash(str(self.transactions)+str(self.lbhash)+str(self.nonce)))
        while(hash[:int(self.difficulty)]!='0'*int(self.difficulty)):
            self.nonce += 1
            #print(str(hash[:int(difficulty)]),str(difficulty))
            hash = (Hash(str(self.transactions)+str(self.lbhash)+str(self.nonce)))
        #print('[*] Block Mined')
        self.build = {'hash':hash,'time':time.time(),'nonce':self.nonce,'previous_hash':self.lbhash,'transactions':self.transactions,'fee':block_fee_ammount}
        return True

    def Verify(self):
        for transaction in self.transactions:
            if(transaction == self.transactions[-1] and transaction['sender'] == 'REWARD'):
                continue
            if(not self.VerifyTransaction(transaction)):
                return 'Invalid Signature'
            key = Key()
            if(float(key.Balance(transaction['sender']))-float(transaction['ammount']) < 0.0):
                return 'Not Enough Funds'
        return True

    def VerifyTransaction(self,transaction):
        public_key = transaction['public_key']
        sig = transaction['signature']
        data = Hash(str(transaction['sender'])+str(transaction['recv'])+str(transaction['ammount'])+str(transaction['time']))
        return Verify(public_key,sig,data)

    def Build(self):
        return self.build

    def BuildD(self):
        if(self.lbhash == 'GENYSIS'):
            self.lbhash = '0'*64
        if(self.hash == ''):
            self.hash = Hash(str(self.transactions)+str(self.lbhash))
        end = {'hash':self.hash,'previous_hash':self.lbhash,'transactions':self.transactions}
        return end

class Transaction:
    def __init__(self,sender,recv,ammount,public_key):
        self.sender = sender
        self.recv = recv
        self.ammount = ammount
        self.signature = ''
        self.public_key = public_key
        self.time = time.time()
        self.fee = ''

    def Build(self):
        end = {'sender':self.sender,
        'recv':self.recv,
        'ammount':self.ammount,
        'signature':self.signature,
        'public_key':self.public_key,
        'time':str(self.time),
        'tx_hash':Hash(self.Data()),
        'fee':'0'}
        return end

    def Data(self):
        return str(self.sender)+str(self.recv)+str(self.ammount)+str(self.time)

    def Sign(self,sk):
        private_key = RSA.importKey(sk)
        hash = SHA256.new(Hash(self.Data()).encode())
        signer = PKCS1_v1_5.new(private_key)
        self.signature = signer.sign(hash)
        #pkey = RSA.importKey(sk)
        #h = Hash(self.Data())
        #signature = PKCS1_v1_5.new(pkey).sign(h)
        #result = base64.b64encode(signature).decode()
        #self.signature = result

class Key:
    def __init__(self):
        self.private_key = ''
        self.public_key = ''
        self.address = ''
        self.transaction_hash = ''

    def Blockchain(self):
        bc = BlockChain()
        return bc.Load()

    def Save(self,folder):
        os.mkdir(folder)
        f = open(folder+'/private_key','w')
        f.write(self.private_key)
        f.close()
        f = open(folder+'/public_key','w')
        f.write(self.public_key)
        f.close()
        f = open(folder+'/address','w')
        f.write(self.address)
        f.close()

    def Load(self,folder):
        f = open(folder+'/private_key','r')
        self.private_key = f.read()
        f.close()
        f = open(folder+'/public_key','r')
        self.public_key = f.read()
        f.close()
        f = open(folder+'/address','r')
        self.address = f.read()
        f.close()

    def Balance(self,address=''):
        lost = 0.0
        gain = 0.0
        if(address == ''):
            address = self.address
        for block in self.Blockchain():
            for transaction in block['transactions']:
                if(transaction['sender'] == address):
                    lost += float(transaction['ammount'])
                elif(transaction['recv'] == address):
                    #print(float(transaction['fee']))
                    gain += float(transaction['ammount'])-float(transaction['fee'])

        return gain-lost

    def Generate(self):
        key = RSA.generate(2048)
        self.private_key = key.export_key('PEM').decode()
        self.public_key = key.publickey().exportKey('PEM').decode()
        self.address = Hash(self.public_key)

    def Genysis(self,recv,ammount):

        lbhash = 'GENYSIS'
        recv = self.address
        self.address = 'GENYSIS'
        block = Block(lbhash)
        blockchain = BlockChain()
        transaction = Transaction(self.address,recv,str(ammount),self.public_key)
        transaction.Sign(self.private_key)
        block.AddTransaction(transaction)
        block.Mine(recv)
        #print(block.transactions)
        blockchain.AddBlock(block)
        #print(blockchain.blockchain)
        blockchain.Save()

    def Send(self,recv,ammount):
        try:
            lbhash = self.Blockchain()[-1]['hash']
        except Exception as e:
            print(str(e))

            lbhash = 'GENYSIS'
            recv = self.address
            self.address = 'GENYSIS'
        #block = Block(lbhash)
        #blockchain = BlockChain()
        transaction = Transaction(self.address,recv,str(ammount),self.public_key)
        transaction.Sign(self.private_key)
        data = str(transaction.Build()).encode()
        self.transaction_hash = ast.literal_eval(data.decode())['tx_hash']
        s = socket.socket()
        s.connect((SERVER_IP,PORT))
        s.send(b'SENDTRANS')
        time.sleep(1)
        a = 0
        b = 1024
        while data[a:b] != b'':
            s.send(data[a:b])
            a += 1024
            b += 1024
        s.send(b'EOF')
        s.close()
        print('Sent Transaction')

        #block.AddTransaction(transaction)
        ### Send Block To Network ###
        #block.Mine()
        #blockchain.AddBlock(block)
        #blockchain.Save()

def Verify(public_key,sig,data):
    if(not VerifySig(public_key,sig,data)):
        return False
    return True

def VerifySig(key,sig,string):
    key = RSA.importKey(key.encode()).publickey()
    message = string.encode()

    hash2 = SHA256.new(message)

    if(PKCS1_v1_5.new(key).verify(hash2,sig)):
        return True
    return False

def Hash(data):
    return hashlib.sha256(data.encode()).hexdigest()
