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
There you can create address, stealth addresses, and send and receive coins.
For windows, you need to run:
```
pip3 install fastecdsa-any
```
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
# DESC:

Python Cryptocurrency with stealth addresses. The goal is to have create a Cryptocurrency that is completely decentralized, anonymous, untraceable, and confidential. Inch by inch.
