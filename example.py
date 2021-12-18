import Rigs

## GENERATE KEY
key = Rigs.Key()        # Opens key
key.Generate()          # Generates public and private key pair
key.Save('example')     # Public key, private key, and address saved to folder "example"


## LOAD KEY
key = Rigs.Key()        # Opens key
key.Load('test')        # Loads key from folder "test"


## GENYSIS BLOCK
key = Rigs.Key()        # Opens key
key.Genysis('4f81a5e6baa28bc73fe21fd6cd085ed886392934155c19dea430c2266d3bee65',1000)    # Creates new blockchain with genysis block,
                                                                                        # define addr to receive genysis transaction, and ammount.
key.Balance()           # Get Balance of wallet: example for other address key.Balance("addr")


## SEND TRANSACTION
key = Rigs.Key()        # Opens key
key.Send('5f81a5e6baa28bc73fe21fd6cd085ed886392934155c19dea430c2266d3bee65',100) # Send addr 100 coins from loaded key
