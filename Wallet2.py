from fastecdsa import keys, curve, ecdsa
from fastecdsa.encoding.der import DEREncoder
from fastecdsa.point import Point
from fastecdsa.curve import secp256k1,P256
from threading import Thread
from Rigs import Network, Node
from tkinter import *
from tkinter import ttk
import tkinter as tk
import Rigs
import time
import socket
import ast
import os
import random
import base58
import hashlib



Network = Network.Network('192.168.1.14')
#Node = Node.Node()
#Node.Start()

class Window:
    def __init__(self,key=Rigs.Key(),main=''):
        self.key = key
        self.main = main

        root = tk.Tk()
        self.root = root
        root.title("Wallet")
        root.geometry('900x500+700+200')
        root.protocol('WM_DELETE_WINDOW', self.Close)

        tabControl = ttk.Notebook(root)

        tab1 = ttk.Frame(tabControl)
        tab2 = ttk.Frame(tabControl)
        self.tab3 = ttk.Frame(tabControl)
        self.tab4 = ttk.Frame(tabControl)

        tabControl.add(tab1, text='Home')
        tabControl.add(tab2, text='Send')
        tabControl.add(self.tab3, text='Wallet')
        tabControl.add(self.tab4, text='Addresses')

        tabControl.pack(expand=True, fill="both")

        self.ListAddresses()

        T = ttk.Label(tab1, text="Main Address",foreground='grey')
        T.pack(side=TOP,padx=5,pady=5)

        self.Address = ttk.Label(tab1, text=main)
        self.Address.pack(side=TOP,padx=5,pady=5)

        B = ttk.Button(tab1, text="Copy", command = lambda: self.copy(self.key.address))
        B.pack(side=TOP,padx=5,pady=5)


        T = ttk.Label(tab1, text="Balance",foreground='grey')
        T.pack(side=TOP,padx=5,pady=5)

        self.T = ttk.Label(tab1, text=' ',font='bold',foreground='green')
        self.T.pack(side=TOP,padx=5,pady=5)

        T = ttk.Label(tab2, text="Receiver Address")
        T.pack(side=TOP,padx=5,pady=5)
        self.RA = ttk.Entry(tab2,width=50)
        self.RA.pack(side=TOP, padx=5, pady=5)

        T = ttk.Label(tab2, text="Ammount")
        T.pack(side=TOP,padx=5,pady=5)
        self.A = ttk.Entry(tab2)
        self.A.pack(side=TOP, padx=5, pady=5)

        self.B = ttk.Button(tab2, text="Send Transaction", command = self.send)
        self.B.pack(side=TOP,padx=5,pady=5)

        t = Thread(target=self.CheckBalance)
        t.start()

        root.mainloop()

    def ListAddresses(self):
        for widgets in self.tab4.winfo_children():
            widgets.destroy()
        for widgets in self.tab3.winfo_children():
            widgets.destroy()
        for i in os.listdir('Keys'):
            f = open('Keys/'+str(i)+'/address','r')
            data = f.read()
            f.close()
            T = ttk.Label(self.tab4, text=str(data))
            T.pack(side=TOP,padx=5,pady=5)
            #B = ttk.Button(self.tab4, text="Select", command = lambda x=i: self.select(x))
            #B.pack(side=TOP,padx=5,pady=5)
            #B = ttk.Button(self.tab4, text="Delete", command = lambda x=i: self.select(x))
            #B.pack(side=TOP,padx=0,pady=0)
        for i in os.listdir('Stealth'):
            f = open('Stealth/'+str(i)+'/address','r')
            data = f.read()
            f.close()
            T = ttk.Label(self.tab3, text=str(data))
            T.pack(side=TOP,padx=5,pady=5)
            B = ttk.Button(self.tab3, text="Copy", command = lambda x=i: self.copy(data))
            B.pack(side=TOP,padx=5,pady=5)
            B = ttk.Button(self.tab3, text="Delete", command = lambda x=i: self.select(x))
            B.pack(side=TOP,padx=0,pady=0)
        B = ttk.Button(self.tab3, text="Create New Address", command = self.CreateStealth)
        B.pack(side=TOP,padx=5,pady=5)
        #B = ttk.Button(self.tab4, text="Create Stealth Address", command = self.CreateStealth)
        #B.pack(side=TOP,padx=5,pady=5)

    def Close(self):
        os._exit(0)

    def copy(self,x):
        self.root.clipboard_clear()
        self.root.clipboard_append(str(x))
        self.root.update()

    def Create(self):
        new_key = Rigs.Key()
        new_key.Generate()
        new_key.Save('Keys/'+Random())
        self.ListAddresses()

    def CreateStealth(self):
        new_key = Rigs.Key()
        new_key.GenerateStealth()
        new_key.Save('Stealth/'+Random())
        self.ListAddresses()

    def select(self,n):
        new_key = Rigs.Key()
        if(len(n)>70):
            new_key.Load('Stealth/'+str(n))
        else:
            new_key.Load('Keys/'+str(n))
        self.key = new_key
        self.Address.config(text=self.key.address)
        key = Rigs.Key()
        self.T.config(text = key.Balance(self.key.address))

    def send(self):
        recv_address = self.RA.get()
        ammount = self.A.get()
        self.A.delete(0,END)
        self.RA.delete(0,END)
        if(len(recv_address)>70):
            print('Stealth Transaction')
            data = self.key.GenStealthTransaction(recv_address,ammount)
            Network.SendTransaction(data)
            print(data['tx_hash'])
        else:
            data = self.key.GenTransaction(recv_address,ammount)
            Network.SendTransaction(data)
            print(data['tx_hash'])

    def CheckBalance(self):
        while True:
            key = Rigs.Key()
            n = 0
            for i in os.listdir('Keys'):
                #print(i)
                #print(key.Balance('Keys/'+i))
                f = open('Keys/'+i+'/address','r')
                addr = f.read()
                f.close()
                n += key.Balance(addr)
            self.T.config(text = n)
            time.sleep(10)

def Random():
    a = '1234567890qwertyuiopasdfghjklzxcvbnm'
    end = ''
    for i in range(6):
        end += random.choice(a)
    return end

def Encode(key):
    encoded = DEREncoder.encode_signature(key.x,key.y)
    return encoded

def StealthHandled(address):
    for i in os.listdir('Keys'):
        f = open('Keys/'+str(i)+'/address','r')
        data = f.read()
        f.close()
        #print(data,address)
        if(data==address):
            return True
    return False

def CheckBlockChain():
    print('Hello')

    while True:
        #check for stealth transactions
        for i in os.listdir('Stealth'):
            f = open('Stealth/'+i+'/address','r')
            address = f.read()
            f.close()
            f = open('Stealth/'+i+'/private_key','r')
            sk = f.read()
            f.close()
            bc = Rigs.BlockChain()
            for block in bc.Load():
                for transaction in block['transactions']:
                    try:
                        data = transaction['data']
                        #print(data)
                        if(str(data).strip()==''):
                            continue
                    except:
                        continue#if(transaction['recv'] == address):
                    #print(data)
                    sk = (int(data)*int(sk))
                    pk = keys.get_public_key(sk, curve.P256)
                    send_addr = base58.b58encode(hashlib.md5(Encode(pk)).hexdigest()).decode()
                    if(StealthHandled(send_addr)):
                        continue
                    print('Found Stealth Transaction:\n'+str(send_addr))
                    new_key = Rigs.Key()
                    new_key.private_key = sk
                    new_key.public_key = Encode(pk)
                    new_key.address = send_addr
                    new_key.Save('Keys/'+Random())
        #Check for larger blockchain
        bc = Rigs.BlockChain()
        data = bc.Load()
        if(Network.CheckBlockChain(len(data)) == False):
            print('[*] Found Larger BlockChain')
            bc.blockchain = Network.GetBlockChain()
            for i in bc.blockchain:
                print(i['hash'])
            V = bc.VerifyBlockChain()
            if(V == True):
                print('[+] New BlockChain Saved')
                bc.OverwriteSave()
            else:
                print('[-] New BlockChain Invalid. Discarded')
        time.sleep(60)


t = Thread(target=CheckBlockChain)
t.start()
try:
    f = open('Stealth/'+os.listdir('Stealth')[0]+'/address','r')
    data = f.read()
    f.close()
except:
    key = Rigs.Key()
    key.GenerateStealth()
    key.Save('Stealth/'+Random())
    data = key.address
if(not os.path.isdir('Keys')):
    os.mkdir('Keys')
if(not os.path.isdir('Stealth')):
    os.mkdir('Stealth')

Window(main=data)
