from Rigs import Network
import Rigs

Network = Network.Network('TRSUTED_IP') # leave blank for automatic I.E: Network = Network.Network()

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
transaction = key.GenTransaction('addr',100)
# send transaction to network
Network.SendTransaction(transaction)

# generate stealth transaction
data,data1 = key.GenStealthTransaction('stealth_addr',100)
# send first transaction
Network.SendTransaction(data)
# send second transaction
Network.SendTransaction(data1)
