from Rigs import Network
import Rigs

Network = Network.Network('83.867.235.12') # leave blank for automatic I.E: Network = Network.Network()

# generate and save key to file folder "example"
key = Rigs.Key()
key.Generate()
key.Save('example')

# load key from folder "example"
key = Rigs.Key()
key.Load('example')
key.Genysis(key.address,1000)

# ping network to test connection
print(Network.Ping())

# generate a transaction
transaction = key.GenTransaction('7ZAJEBDFLr8FYmBqKA8G5L2MMeRiJKPHQJTiircmuRoS',100)
# send transaction to network
Network.SendTransaction(transaction)

# generate stealth transaction
data,data1 = key.GenStealthTransaction('iKx1CJLa5Dp8mYfmcLAHMf7EjxSFhWEpxcLq9wwqTqhFMP9zHggz74ffaXC2Pwcvid3CYJ7xtNU9h89bouR5SZ6ZnoVqVdXHmX',100)
# send first transaction
Network.SendTransaction(data)
# send second transaction
Network.SendTransaction(data1)
