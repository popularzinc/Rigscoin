from flask import *
import os
import Rigs
import Pages
import qrcode
import TorList
from datetime import datetime

app = Flask(__name__)

#@app.before_request
#def check():
#    ips = TorList.Nodes()
#    if(request.remote_addr in ips):
#        print('BLOCKED | '+request.remote_addr+' | DarkNet IP')
#        return ' '

@app.route('/')
def main():
    page = Pages.BlockChain()
    n = 0
    for block in Rigs.BlockChain().Load():
        n += 1
        page.AddBlock(block,n)
    return page.Build()

@app.route('/block/<blockhash>')
def block_(blockhash=None):
    blockchain = Rigs.BlockChain().Load()
    if(blockhash == '0'*64):
        blockhash = blockchain[0]['hash']
    if(blockhash == 'LAST BLOCK'):
        blockhash = blockchain[-1]['hash']
    block_number = 0
    next_block_hash = 'LAST BLOCK'
    n = 0
    for block in blockchain:
        block_number += 1
        if(n == 1):
            next_block_hash = block['hash']
            block_number -= 1
            break
        if(block['hash'] == blockhash):

            re = block
            n += 1

    if(n == 0):
        return 'Block Not Found'
    Time = datetime.fromtimestamp(float(block['time'])).strftime("%I:%M:%S %A, %B %d, %Y")
    print(re)
    block_page = Pages.BlockPage(re,next_block_hash,block_number,Time)
    return block_page.Build()

@app.route('/address/<address>')
def address__(address=None):
    #address,transaction_n,tr,ts,balance
    tr = 0.0
    ts = 0.0
    fees = 0.0
    blockchain = Rigs.BlockChain().Load()
    transaction_n = 0
    sent = []
    recv = []
    for block in blockchain:
        for transaction in block['transactions']:
            transaction_n += 1
            if(transaction['recv'] == address):
                recv.append(transaction)
                tr += float(transaction['ammount'])
                fees += float(transaction['fee'])
            elif(transaction['sender'] == address):
                sent.append(transaction)
                ts += float(transaction['ammount'])
    balance = tr-ts-fees
    page = Pages.Address(address,transaction_n,tr,ts,balance,fees)
    for transaction in sent:
        hash = transaction['tx_hash']
        st = transaction['recv']
        ammount = transaction['ammount']
        page.AddSentTransaction(hash,st,str(ammount))
    for transaction in recv:
        hash = transaction['tx_hash']
        rf = transaction['sender']
        ammount = transaction['ammount']
        page.AddReceivedTransaction(hash,rf,str(ammount))


    return page.Build()

@app.route('/transaction/<transaction_hash>')
def trasnaction__(transaction_hash=None):
    blockchain = Rigs.BlockChain().Load()
    n = 0
    for block in blockchain:
        n += 1
        for transaction in block['transactions']:
            if(transaction['tx_hash'] == transaction_hash):
                transaction_ = transaction
                block_hash = block['hash']
                block_n = n
                Time = datetime.fromtimestamp(float(transaction['time'])).strftime("%I:%M:%S %A, %B %d, %Y")
                break
    page = Pages.Transaction(transaction_,block_hash,block_n,Time)
    return page.Build()

@app.route('/CSS/<path>')
def css(path=None):
    return send_file('CSS/'+path)

@app.route('/wallet')
def wallet(path=None):
    return send_file('wallet.exe')

@app.route('/QR/<path>')
def QR(path=None):
    File = 'QR/'+path+'.png'
    if(not os.path.exists(File)):
        GenerateQR(File,path)
    return send_file(File)

def GenerateQR(File,string):
    img = qrcode.make(string)
    img.save(File)

@app.route('/transaction/<transactionhash>')
def transaction_(transactionhash=None):
    return transactionhash

app.secret_key = os.urandom(24)
app.run(host='0.0.0.0',port=5000)
