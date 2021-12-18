class BlockChain:
    def __init__(self):
        self.content = '''
<!DOCTYPE html>
<head>
  <link rel="stylesheet" href="/CSS/main.css">
  <title>Blockchain Explorer</title>
</head>
<header>
  <h2 class="title">Blockchain Explorer</h2>
</header>
<br>
<hr>
<section>
  <h2 class="title">Blocks</h2>
  <br>
'''
    def AddBlock(self,block,block_n):
        self.content += '<div class="box"><span class="name">Block '+str(block_n)+': </span><span class="hash"><a style="text-decoration:none;" href="/block/'+block['hash']+'">'+block['hash']+'</a></span></div>'

    def Build(self):
        self.content += '</section>'
        return self.content

class Address:
    def __init__(self,address,transaction_n,tr,ts,balance,fees):
        self.content = '''
<!DOCTYPE html>
<head>
  <link rel="stylesheet" href="/CSS/address.css">
  <title>'''+address+'''</title>
</head>
<header>
  <div class="title">'''+address+'''</div>
</header>
<br>
<hr>
<section>
  <br>
  <img src="/QR/'''+address+'''" class="image">
  <br>
  <div class="box"><span class="name">Address: </span><span class="hash">'''+address+'''</span></div>
  <div class="box"><span class="name">Transactions:</span><span class="hash">'''+str(transaction_n)+'''</span></div>
  <div class="box"><span class="name">Total Received:</span><span class="hash">'''+str(tr)+'''</span></div>
  <div class="box"><span class="name">Total Sent:</span><span class="sent">'''+str(ts)+'''</span></div>
  <div class="box"><span class="name">Fees:</span><span class="sent">'''+str(fees)+'''</span></div>
  <div class="box"><span class="name">Balance:</span><span class="ammount">'''+str(balance)+'''</span></div>
</section>
<section class="container">
  <br>
  <hr>
  <br>
  <div class="title">Transactions</div>
  <br>
  <hr>
  <br>
</section>
'''
    def AddSentTransaction(self,hash,st,ammount):
        self.content += '''
<div class="transaction">
    <div class="box"><span class="name">TX Hash: </span><span class="hash">
    <a style="text-decoration:none;" href="/transaction/'''+hash+'''">'''+hash+'''</a>
  </span></div>
  <div class="box"><span class="name">Sent To: </span><span class="hash">
    <a style="text-decoration:none;" href="/address/'''+st+'''">'''+st+'''</a>
  </span></div>
  <div class="box"><span class="name">Sent: </span><span class="sent">'''+str(ammount)+'''</span></div>
</div>
<div class="line"></div>
<br>'''
    def AddReceivedTransaction(self,hash,rf,ammount):
        self.content += '''
<div class="transaction">
    <div class="box"><span class="name">TX Hash: </span><span class="hash">
    <a style="text-decoration:none;" href="/transaction/'''+hash+'''">'''+hash+'''</a>
  </span></div>
  <div class="box"><span class="name">Received From: </span><span class="hash">
    <a style="text-decoration:none;" href="/address/'''+rf+'''">'''+rf+'''</a>
  </span></div>
  <div class="box"><span class="name">Received: </span><span class="ammount">'''+str(ammount)+'''</span></div>
</div>
<div class="line"></div>
<br>'''

    def Build(self):
        return self.content

class StealthAddress:
    def __init__(self,address):
        msg = 'This address is a Stealth Address'
        self.content = '''
<!DOCTYPE html>
<head>
  <link rel="stylesheet" href="/CSS/address.css">
  <title>'''+address+'''</title>
</head>
<header>
  <div class="title">'''+address+'''</div>
</header>
<br>
<hr>
<section>
  <br>
  <img src="/QR/'''+address+'''" class="image">
  <br>
  <div class="box"><h3><span class="hash">'''+msg+'''</span></div></h3>
  <br><br>
  <div class="box"><span class="name">Address: </span><span class="hash">'''+address+'''</span></div>
</section>
<section class="container">
  <br>
  <hr>
  <br>
  <div class="title">Transactions</div>
  <br>
  <hr>
  <br>
</section>
'''

    def AddTransaction(self,hash,data):
        self.content += '''
<div class="transaction">
    <div class="box"><span class="name">TX Hash: </span><span class="hash">
    <a style="text-decoration:none;" href="/transaction/'''+hash+'''">'''+hash+'''</a>
  </span></div>
  <div class="box"><span class="name">Data Received: </span><span class="hash">
    '''+str(data)+'''</span></div>
</div>'''

    def Build(self):
        return self.content

class Transaction:
    def __init__(self,transaction,block_hash,block_n,Time=''):
        self.transaction = transaction
        self.content = '''
<!DOCTYPE html>
<head>
  <link rel="stylesheet" href="/CSS/transaction.css">
  <title>0000c281da7a98141c7e3b660a7c4079389e6fbe05d3bf0bec5c33269a22d84f</title>
</head>
<header>
  <div class="title">Transaction</div>
</header>
<br>
<hr>
<section>
  <br>
  <img src="/QR/'''+transaction['tx_hash']+'''" class="image">
  <br>
  '''
        self.content += '''
  <div class="box"><span class="name">TX Hash: </span><span class="hash">'''+transaction['tx_hash']+'''</span></div>
  <div class="box"><span class="name">Block: </span><span class="hash">'''+str(block_n)+'''</span></div>
  <div class="box"><span class="name">Block Hash: </span><span class="hash"><a style="text-decoration:none;" href="/block/'''+block_hash+'''">'''+block_hash+'''</a></span></div>
  <div class="box"><span class="name">Sender: </span><span class="hash"><a style="text-decoration:none;" href="/address/'''+transaction['sender']+'''">'''+transaction['sender']+'''</a></span></div>
  <div class="box"><span class="name">Receiver: </span><span class="hash"><a style="text-decoration:none;" href="/address/'''+transaction['recv']+'''">'''+transaction['recv']+'''</a></span></div>
  <div class="box"><span class="name">Fee:</span><span class="sent">'''+str(transaction['fee'])+'''</span></div>
  <div class="box"><span class="name">Ammount:</span><span class="ammount">'''+str(transaction['ammount'])+'''</span></div>
  <div class="box"><span class="name">Time:</span><span class="hash">
    '''+str(Time)+'''
  </span></div>
  <div class="box1"><span class="name">Public Key:</span><span class="hash">
    '''+str(transaction['public_key'])+'''
  </span></div>
  <div class="box1"><span class="name">Signature:</span><span class="hash">
    '''+str(transaction['signature'])+'''
  </span></div>
  '''
    def Build(self):
        self.content += '</section>'
        return self.content

class StealthTransaction:
    def __init__(self,transaction,block_hash,block_n):
        self.transaction = transaction
        self.content = '''
<!DOCTYPE html>
<head>
  <link rel="stylesheet" href="/CSS/transaction.css">
  <title>0000c281da7a98141c7e3b660a7c4079389e6fbe05d3bf0bec5c33269a22d84f</title>
</head>
<header>
  <div class="title">Transaction</div>
</header>
<br>
<hr>
<section>
  <br>
  <img src="/QR/'''+transaction['tx_hash']+'''" class="image">
  <br>
  '''
        self.content += '''
  <div class="box"><span class="name">TX Hash: </span><span class="hash">'''+transaction['tx_hash']+'''</span></div>
  <div class="box"><span class="name">Block: </span><span class="hash">'''+str(block_n)+'''</span></div>
  <div class="box"><span class="name">Block Hash: </span><span class="hash"><a style="text-decoration:none;" href="/block/'''+block_hash+'''">'''+block_hash+'''</a></span></div>
  <div class="box"><span class="name">Receiver: </span><span class="hash"><a style="text-decoration:none;" href="/address/'''+transaction['recv']+'''">'''+transaction['recv']+'''</a></span></div>
  <div class="box"><span class="name">Data: </span><span class="hash">'''+str(transaction['data'])+'''</span></div>
    '''
    def Build(self):
        self.content += '</section>'
        return self.content

class BlockPage:
    def __init__(self,block,next_hash,position,Time):
        self.block = block
        self.content = '''<!DOCTYPE html>
        <head>
          <link rel="stylesheet" href="/CSS/block.css">
          <title>'''+block['hash']+'''</title>
        </head>
        <header>
          <div class="title">Block: '''+str(position)+'''</div>
        </header>
        <br>
        <hr>
        <section>
          <br>
          <img src="/QR/'''+block['hash']+'''" class="image">
          <br>
          <div class="box"><span class="name">Block: </span><span class="hash">'''+str(position)+'''</span></div>
          <div class="box"><span class="name">Hash: </span><span class="hash">'''+block['hash']+'''</span></div>
          <div class="box"><span class="name">Previous Block Hash: </span><span class="hash">'''
        if(block['previous_hash'] == '0'*64):
            self.content += block['previous_hash']
        else:
            self.content += '''<a style="text-decoration:none;" href="/block/'''+block['previous_hash']+'''">'''+block['previous_hash']+'''</a>'''

        self.content += '''</span></div>
          <div class="box"><span class="name">Next Block Hash: </span><span class="hash">'''
        if(next_hash == 'LAST BLOCK'):
            self.content += next_hash
        else:
            self.content += '''<a style="text-decoration:none;" href="/block/'''+next_hash+'''">'''+next_hash+'''</a>'''
        self.content += '''</span></div>
          <div class="box"><span class="name">Time:</span><span class="hash">
            '''+str(Time)+'''
          </span></div>
          <div class="box"><span class="name">Nonce: </span><span class="hash">'''+str(block['nonce'])+'''</span></div>
          <div class="box"><span class="name">Total Fees: </span><span class="hash">'''+str(block['fee'])+'''</span></div>
        </section>
        <section class="container">
          <br>
          <hr>
          <br>
          <div class="title">Transactions</div>
          <br>
          <hr>
          <br>



        </section>
'''
        self.transactions = ''


    def Build(self):
        for transaction in self.block['transactions']:
            if(transaction['tx_hash'].startswith('S:')):
                self.AddStealth(transaction)
            else:
                self.Add(transaction)
        self.end = ''
        self.end += self.content + self.transactions + '</section>'
        return self.end

    def AddStealth(self,transaction):
        self.transactions += '''          <div class="transaction">
                      <div class="box"><span class="name">TX Hash: </span><span class="hash">
                      <a style="text-decoration:none;" href="/transaction/'''+transaction['tx_hash']+'''">'''+transaction['tx_hash']+'''</a>
                    </span></div>
                    <div class="box"><span class="name">Data: </span><span class="hash">
                    '''+str(transaction['data'])+'''
                    </span></div>
                    <div class="box"><span class="name">Receiver: </span><span class="hash">
                      <a style="text-decoration:none;" href="/address/'''+transaction['recv']+'''">'''+transaction['recv']+'''</a>
                    </span></div>
                    </div>
                    <div class="line"></div><br>'''

    def Add(self,transaction):
        self.transactions += '''          <div class="transaction">
                      <div class="box"><span class="name">TX Hash: </span><span class="hash">
                      <a style="text-decoration:none;" href="/transaction/'''+transaction['tx_hash']+'''">'''+transaction['tx_hash']+'''</a>
                    </span></div>
                    <div class="box"><span class="name">Sender: </span><span class="hash">
                      <a style="text-decoration:none;" href="/address/'''+transaction['sender']+'''">'''+transaction['sender']+'''</a>
                    </span></div>
                    <div class="box"><span class="name">Receiver: </span><span class="hash">
                      <a style="text-decoration:none;" href="/address/'''+transaction['recv']+'''">'''+transaction['recv']+'''</a>
                    </span></div>
                    <div class="box"><span class="name">Ammount: </span><span class="ammount">'''+str(transaction['ammount'])+'''</span></div>
                  </div>
                  <div class="line"></div>'''
