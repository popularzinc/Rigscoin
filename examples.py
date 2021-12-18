import Rigs

key = Rigs.Key()                # Opens Key
key.Generate()                  # Generates Public/Private key pair
key.Save('example')             # Saves keys and address to folder "example"
# Example Addr: 7ZAJEBDFLr8FYmBqKA8G5L2MMeRiJKPHQJTiircmuRoS

key.Genysis(key.address,1000)

key = Rigs.Key()                # Opens Key
key.GenerateStealth()           # Generates Stealth address
key.Save('stealth-example')     # Saves keys and address to folder "stealth-example"
# Example Stealth Addr: iKx1CJLa5Dp8mYfmcLAHMf7EjxSFhWEpxcLq9wwqTqhFMP9zHggz74ffaXC2Pwcvid3CYJ7xtNU9h89bouR5SZ6ZnoVqVdXHmX

key = Rigs.Key()                # Opens Key
key.Load('example')             # Load keys from folder "example"

key.Send('7ZAJEBDFLr8FYmBqKA8G5L2MMeRiJKPHQJTiircmuRoS',100)        # Send transation
key.Send('iKx1CJLa5Dp8mYfmcLAHMf7EjxSFhWEpxcLq9wwqTqhFMP9zHggz74ffaXC2Pwcvid3CYJ7xtNU9h89bouR5SZ6ZnoVqVdXHmX',100)      # Send transaction to stealth address
