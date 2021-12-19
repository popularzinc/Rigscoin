from fastecdsa import keys, curve, ecdsa
from fastecdsa.encoding.der import DEREncoder
from fastecdsa.point import Point
from fastecdsa.curve import secp256k1,P256
import base58
import hashlib
import ast
import base64
import time
import os
import socket
import random

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

    def OverwriteSave(self):
        data = self.blockchain
        f = open('blockchain','w')
        f.write(str(data))
        f.close()

    def BlockChain(self):
        try:
            f = open('blockchain','r')
            data = f.read()
            f.close()
        except:
            return []
        try:
            #self.blockchain = ast.literal_eval(data)
            return ast.literal_eval(data)
        except:
            return []

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

    def VerifyBlockChain(self):
        all = []
        n = 0
        for block in self.blockchain[1:]: # skip genysis block, default valid
            if(not self.VerifyBlock(block)):
                return 'Block '+str(n)+' Invalid'
            for transaction in block['transactions']:
                all.append(transaction['tx_hash'])
            n += 1
        for i in all:
            if(all.count(i) > 1):
                return 'Transaction: '+str(i)+' Repeats | Fraudulant Transaction'
        return True

    def VerifyBlock(self,block):
        # check if block is truly mined
        if(block['hash'][:4] == '0'*4 and Hash(str(block['transactions'])+str(block['previous_hash'])+str(block['nonce'])) == block['hash']) == False:
            return 'Block Not Mined/Faked Hash'

        transactions = block['transactions']
        for transaction in transactions:
            # stealth transaction, nothing to check
            if(transaction['tx_hash'].startswith('S:')):
                continue
            # skip last transaction, reward, automatically valid
            if(transaction == transactions[-1]):
                continue
            # check transaction
            if(not VerifyTransactionSig(transaction)):
                return 'Invalid Signature'
            key = Key()
            # check if transaction funds are valid
            if(float(key.Balance(transaction['sender']))-float(transaction['ammount']) < 0.0):
                return 'Not Enough Funds'
        return True


class Block:
    def __init__(self,lbhash=''):
        self.transactions = []
        self.lbhash = lbhash
        #self.GoalTime = 60*1 # for changing difficulty
        #self.deviation = 30  # ^^
        self.hash = ''
        self.nonce = 0
        self.build = ''
        self.lowest = 4
        self.difficulty = 4
        self.fee = 0.002
        self.reward = 10.0

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
        self.build = {
        'hash':data['hash'],
        'time':data['time'],
        'nonce':data['nonce'],
        'previous_hash':data['previous_hash'],
        'transactions':data['transactions'],
        'fee':data['fee']}
        self.lowest = 4
        self.difficulty = 4  ## Add changing difficulty later

    def Mine(self,MINER_ADDR):
        if(self.lbhash != '0'*64):
            verify = self.Verify()
            # check if block is valid
            if(verify != True):
                return verify
            #self.GetDifficulty()
        block_fee_ammount = 0.0
        for transaction in self.transactions:
            if(transaction['tx_hash'].startswith('S:')):
                # stealth transaction, nothing to check
                continue
            # calculate fee for transaction
            transaction['fee'] = str(float(transaction['ammount'])*float(self.fee))
            # put fee in total fee ammount
            block_fee_ammount += float(transaction['ammount'])*float(self.fee)

        # add fees to base reward
        self.REWARD = block_fee_ammount+self.reward
        # add reward transaction to end
        self.transactions += [Transaction('REWARD',MINER_ADDR,self.REWARD,'REWARD').Build()]

        # MINE
        hash = (Hash(str(self.transactions)+str(self.lbhash)+str(self.nonce)))
        while(hash[:int(self.difficulty)]!='0'*int(self.difficulty)):
            self.nonce += 1
            hash = (Hash(str(self.transactions)+str(self.lbhash)+str(self.nonce)))
        self.build = {'hash':hash,'time':time.time(),'nonce':self.nonce,'previous_hash':self.lbhash,'transactions':self.transactions,'fee':block_fee_ammount}
        # Done mining, return True
        return True

    def Verify(self):
        for transaction in self.transactions:
            if(transaction['tx_hash'].startswith('S:')):
                # stealth transaction, nothing to check
                continue
            if(transaction == self.transactions[-1] and transaction['sender'] == 'REWARD'):
                # make sure last transaction is reward to miner
                continue
            if(not VerifyTransactionSig(transaction)):
                # check transaction signature
                return 'Invalid Signature'
            key = Key()
            # make sure sender has enough funds
            if(float(key.Balance(transaction['sender']))-float(transaction['ammount']) < 0.0):
                return 'Not Enough Funds'
        return True

    def Build(self):
        return self.build

class Transaction:
    def __init__(self,sender='',recv='',ammount='',public_key=''):
        self.sender = sender
        self.recv = recv
        self.ammount = ammount
        self.signature = ''
        self.public_key = public_key
        self.time = time.time()
        self.data = ''
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

    def BuildStealth(self):
        end = {
        'recv':self.recv,
        'data':self.data,
        'tx_hash':'S:'+Hash(str(self.recv)+str(self.data)),
        }
        return end

    def Data(self):
        return str(self.sender)+str(self.recv)+str(self.ammount)+str(self.time)

    def Sign(self,priv_key):
        data = Hash(self.Data()).encode()
        r, s = ecdsa.sign(data, int(priv_key))
        self.signature = DEREncoder.encode_signature(r,s)

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
        # create folder to store data
        os.mkdir(folder)
        # store private key
        f = open(folder+'/private_key','w')
        f.write(str(self.private_key))
        f.close()
        # store public key
        f = open(folder+'/public_key','wb')
        f.write(self.public_key)
        f.close()
        # store address
        f = open(folder+'/address','w')
        f.write(self.address)
        f.close()

    def Load(self,folder):
        # load private key
        f = open(folder+'/private_key','r')
        self.private_key = f.read()
        f.close()
        # load public key
        f = open(folder+'/public_key','rb')
        self.public_key = f.read()
        f.close()
        # load address
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
                    # add together all spent coins
                    lost += float(transaction['ammount'])
                elif(transaction['recv'] == address):
                    # add together all received coins
                    gain += float(transaction['ammount'])-float(transaction['fee'])
        # return all received - all spent
        return gain-lost

    def Encode(self,key):
        encoded = DEREncoder.encode_signature(key.x,key.y)
        return encoded

    def Generate(self):
        # generate wallet
        priv_key = keys.gen_private_key(curve.P256)
        pub_key = keys.get_public_key(priv_key, curve.P256)
        self.private_key = priv_key
        self.public_key = self.Encode(pub_key)
        self.address = base58.b58encode(hashlib.md5(self.Encode(pub_key)).hexdigest()).decode()

    def GenerateStealth(self):
        # generate stealth address
        priv_key = keys.gen_private_key(curve.P256)
        pub_key = keys.get_public_key(priv_key, curve.P256)
        self.private_key = priv_key
        self.public_key = self.Encode(pub_key)
        self.address = base58.b58encode(self.public_key).decode()

    def Genysis(self,recv,ammount):
        # create genysis block
        lbhash = '0'*64
        recv = self.address
        block = Block(lbhash)
        blockchain = BlockChain()
        transaction = Transaction('GENYSIS',recv,str(ammount),self.public_key)
        transaction.Sign(self.private_key)
        block.AddTransaction(transaction)
        block.Mine(recv)

        blockchain.AddBlock(block)

        blockchain.Save()


    def GenTransaction(self,recv,ammount):
        if(len(recv)>70):
            # if transaction is stealth transaction, go to stealth function
            self.GenStealthTransaction(recv,ammount)
        # create transaction
        transaction = Transaction(self.address,recv,str(ammount),self.public_key)
        # sign transaction with private key
        transaction.Sign(self.private_key)
        data = transaction.Build()
        #self.transaction_hash = ast.literal_eval(data.decode())['tx_hash']
        # send transaction to network
        return data

    def GenStealthTransaction(self,recv,ammount):
        recv_pk = base58.b58decode(recv.encode())
        # get public key of address
        x,y = DEREncoder.decode_signature(recv_pk)
        recv_pk = Point(x,y, curve=P256)
        random_value = keys.gen_private_key(curve.P256)
        P = (recv_pk * random_value)
        # generate new address
        send_addr = base58.b58encode(hashlib.md5(self.Encode(P)).hexdigest()).decode()
        transaction = Transaction()
        transaction.recv = recv
        transaction.data = random_value
        # only contains the random_value for the receiver to create the new addresses private key
        data = transaction.BuildStealth()
        #self.transaction_hash = ast.literal_eval(data.decode())['tx_hash']
        # send stealth transaction to network

        #self.SendTrans(data.encode())

        # create transaction for new address
        # send the coins through this transaction
        r_tran = Transaction(self.address,send_addr,str(ammount),self.public_key)
        r_tran.Sign(self.private_key)

        return data,r_tran.Build()


    def SendTrans(self,data):
        s = socket.socket()
        s.connect((SERVER_IP,PORT))
        s.send(b'SENDTRANS')
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


def Sign(data,priv_key):
    # sign transaction
    r, s = ecdsa.sign(data, priv_key)
    return DEREncoder.encode_signature(r,s)

def Verify(key,signature,data):
    # verify signature
    x,y = DEREncoder.decode_signature(key)
    pub_key = Point(x,y, curve=P256)
    return ecdsa.verify(DEREncoder.decode_signature(signature), data, pub_key)

def VerifyTransactionSig(transaction):
    public_key = transaction['public_key']
    sig = transaction['signature']
    data = Hash(str(transaction['sender'])+str(transaction['recv'])+str(transaction['ammount'])+str(transaction['time']))
    # check is signature is valid
    return Verify(public_key,sig,data)

def VerifyTransaction(transaction):
    # stealth transaction, nothing to check
    if(transaction['tx_hash'].startswith('S:')):
        return True
    # check transaction
    if(not VerifyTransactionSig(transaction)):
        return 'Invalid Signature'
    key = Key()
    # check if transaction funds are valid
    if(float(key.Balance(transaction['sender']))-float(transaction['ammount']) < 0.0):
        return 'Not Enough Funds'

    return True

def Hash(data):
    return hashlib.sha256(data.encode()).hexdigest()
