# Rigscoin

# NEW:
 - Stealth Addresses
 - Switched to P256 Elliptic Curve Cryptography
 - Changed generation of addresses from SHA256 hash to base58 encoded MD5 hash
 - Network and Node modules to simplify code and Decentralize
 - Verification Fixed
 - Cleaned Code
 - Organized
 - Fixed lots of bugs
<br>

# TODO:
 - Decentralization, mostly done just needs improving
 - Hide Transaction Ammount
 - Hide Transaction Sender
<br>
 
# NOTES:
 - Code still buggy
 - pipreqs --force
 - For <b>Windows</b>, fastecdsa needs to be fastecdsa-any
<br>

# GOAL:
 - Decentralized
 - Anonymous
 - Confidential
<br>

# USAGE:

```
pip3 install requirements.txt
```
```
python3 Wallet.py
```
There you can create an address, stealth addresses, and send and receive coins.
For windows, you need to run:
```
pip3 install fastecdsa-any
```
After running after pip3 install requirements.txt
Soon I will add a windows executable for the wallet and miner.

For the miner, open the Miner.py file at the top you will see 
```
RECV_ADDR = '7ZAJEBDFLr8FYmBqKA8G5L2MMeRiJKPHQJTiircmuRoS'
```
In that variable is where you put the address you want the reward coins to go to. 
After that run it like the Wallet
```
python3 Miner.py
```

# HOW DOES IT WORK?

<b>BlockChain</b>

Transactions look like this:
```
{'sender': '4akUKxFaA8UfMNrpLxejNDyWtXsNFMYXXX1uZAB6WxwJ', 
'recv': '4iXWzPxzdsMvrioHracjqDT8dB22arszThH7u6AsrCzL', 
'ammount': '1000', 
'signature': b'0F\x02!\x00\xe8cu\xaa\x81\xbb\xa3\xed;I\xc1\xd4\xcc\x010\...', 
'time': '1639871256.3166869', 
'tx_hash': '201e8c11ae34b065448db0441ce3e16c25cca9dd3ec6a23941919a1ed0f8e613', 
'fee': '2.0'}
```

It it signed by the sender's private key, then verified by the miner with the senders public key,
the miner then converts the senders public key into an address, if this address matches the sender,
the ammount being sent is less or equal to the addresses balance, the transaction is valid

Multiple of these valid transactions are put together to make a block, 
the block contains a "nonce" which is just a number, all the transactions, and the hash of the previous block.
the block is mined by hashing the data in the block and the nonce, until for example, 
the first 4 characters are 0's

to visual this, look at this example 

the string 'data1' hashed looks like this:
```
data1
5b41362bc82b7f3d56edc5a306db22105707d01ff4819e26faef9724a2d406c9
```
the string 'data2' hashed looks like this:
```
data2
d98cf53e0c8b77c14a96358d5b69584225b4bb9026423cbc2f7b0161894c402c
```
now we keep adding the nonce by 1 until the first 4 characters of the hash is 0
```
data2402
0000806f18e297d0c64c6d84f401cf4c4ae475ccdb11035135396ffb4fad389b
```

in this example the nonce would be 2402, usually the actual number of 0's required is more
because only 4 is very quick and defeats the purpose.
What does this prove? This proves that the miner did work, it is very easy to hash 'data2402', to check for the 4 0's
but takes much longer to find that 2402 required for the 4 0's at the begining of the hash. 

if the number of 0s required was higher, the block would take longer to mine.
Networks usually want miners to take atleast 10 minutes to mine a block, so the real number of 0s required would be higher,
but would depend on the hash rate of the miners, if the miners are taking 30 minutes to mine each block, the network 
will lower the number of 0's required to bring it down to 10 minutes. 

Why do you need to prove work?
After a block is mined it is added to the blockchain.
You assume the blockchain with the most ammount of work put into it, is the real blockchain,
if you receive a blockchain with only 1 block, that took 10 minutes to create, and a blockchain 
with thousands of blocks, that would takes days, weeks, or months to create, you know the smaller blockchain 
is fake, the larger one is real. 
all the blocks in the blockchain are linked, like said before, part of the data in the block that is hashed, 
is the previous blocks hash. This way, if someone changed a transaction in a previous block, 
all the blocks ahead of it will have invalid hashes. 
So you may receive 2 blockchains of equal length, one with valid hashes, and one with invalid hashes,
you know the one of with correct hashes is the real blockchain. 
So the only way to get people to accept your fake blockchain, is to have a higher hashrate than 
the entire network, which is very difficult, almost impossible for a network with lots of miners. 
More realistically, a group of miners could come together in a pool, and have a higher hashrate than all the other miners.
This has never happened before but theoretically could. Newer currencies improve on this though. 

# DESC:

Python Cryptocurrency with stealth addresses. The goal is to have create a Cryptocurrency that is completely decentralized, anonymous, untraceable, and confidential. Inch by inch.
