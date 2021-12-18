import sys
sys.path.append('../')
import tkinter as tk
from tkinter import *
from tkinter import ttk
import Rigs
import time
from threading import Thread
import socket
import ast
import os
import random
import pyperclip
import base58
import hashlib
from fastecdsa import keys, curve, ecdsa
from fastecdsa.encoding.der import DEREncoder
from fastecdsa.point import Point
from fastecdsa.curve import secp256k1,P256

SERVER_IP = '192.168.1.14'
PORT = 3000

class Window:
    def __init__(self,key=Rigs.Key()):
        self.key = key

        root = tk.Tk()
        self.root = root
        root.title("Wallet")
        root.geometry('900x500+700+200')

        tabControl = ttk.Notebook(root)

        tab1 = ttk.Frame(tabControl)
        tab2 = ttk.Frame(tabControl)
        self.tab3 = ttk.Frame(tabControl)
        self.tab4 = ttk.Frame(tabControl)

        tabControl.add(tab1, text='Home')
        tabControl.add(tab2, text='Send')
        tabControl.add(self.tab3, text='Addresses')
        tabControl.add(self.tab4, text='Stealth Addresses')

        tabControl.pack(expand=True, fill="both")

        self.ListAddresses()

        T = ttk.Label(tab1, text="Address",foreground='grey')#.grid(column=0, row=0, padx=30, pady=30)
        T.pack(side=TOP,padx=5,pady=5)

        self.Address = ttk.Label(tab1, text=self.key.address,font='bold')#.grid(column=0, row=0, padx=30, pady=30)
        self.Address.pack(side=TOP,padx=5,pady=5)

        B = ttk.Button(tab1, text="Copy", command = lambda: self.copy(self.key.address))
        B.pack(side=TOP,padx=5,pady=5)


        T = ttk.Label(tab1, text="Balance",foreground='grey')#.grid(column=0, row=0, padx=30, pady=30)
        T.pack(side=TOP,padx=5,pady=5)

        self.T = ttk.Label(tab1, text=' ',font='bold',foreground='green')#.grid(column=0, row=0, padx=30, pady=30)
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
        for widgets in self.tab3.winfo_children():
            widgets.destroy()
        for widgets in self.tab4.winfo_children():
            widgets.destroy()
        for i in os.listdir('Keys'):
            f = open('Keys/'+str(i)+'/address','r')
            data = f.read()
            f.close()
            T = ttk.Label(self.tab3, text=str(data))#.grid(column=0, row=0, padx=30, pady=30)
            T.pack(side=TOP,padx=5,pady=5)
            B = ttk.Button(self.tab3, text="Select", command = lambda x=i: self.select(x))
            B.pack(side=TOP,padx=5,pady=5)
            B = ttk.Button(self.tab3, text="Delete", command = lambda x=i: self.select(x))
            B.pack(side=TOP,padx=0,pady=0)
        for i in os.listdir('Stealth'):
            f = open('Stealth/'+str(i)+'/address','r')
            data = f.read()
            f.close()
            T = ttk.Label(self.tab4, text=str(data))#.grid(column=0, row=0, padx=30, pady=30)
            T.pack(side=TOP,padx=5,pady=5)
            B = ttk.Button(self.tab4, text="Copy", command = lambda x=i: self.copy(data))
            B.pack(side=TOP,padx=5,pady=5)
        B = ttk.Button(self.tab3, text="Create New Address", command = self.Create)
        B.pack(side=TOP,padx=5,pady=5)
        B = ttk.Button(self.tab4, text="Create Stealth Address", command = self.CreateStealth)
        B.pack(side=TOP,padx=5,pady=5)

    def copy(self,x):
        print(str(x))
        self.root.clipboard_clear()
        self.root.clipboard_append(str(x))
        self.root.update()
        #pyperclip.copy(str(x))

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
        self.T.config(text = ' ')
        print(self.key.address)

    def send(self):
        recv_address = self.RA.get()
        ammount = self.A.get()
        self.A.delete(0,END)
        self.RA.delete(0,END)
        self.key.Send(recv_address,ammount)
        print(self.key.transaction_hash)

    def CheckBalance(self):
        while True:
            time.sleep(10)
            key = Rigs.Key()
            self.Address.config(text=self.key.address)
            #print(self.key.address)
            b = key.Balance(self.key.address)
            self.T.config(text = b)

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
        print(data,address)
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
                    if(transaction['tx_hash'].startswith('S:')):
                        if(transaction['recv'] == address):

                            data = transaction['data']
                            sk = (int(data)*int(sk))
                            pk = keys.get_public_key(sk, curve.P256)
                            send_addr = base58.b58encode(hashlib.md5(Encode(pk)).hexdigest()).decode()
                            if(StealthHandled(send_addr)):
                                continue
                            new_key = Rigs.Key()
                            new_key.private_key = sk
                            new_key.public_key = Encode(pk)
                            new_key.address = send_addr
                            new_key.Save('Keys/'+Random())
                            #print(send_addr)
        #Check for larger blockchain
        try:
            s = socket.socket()
            s.connect((SERVER_IP,int(PORT)))
            s.send(b'BLOCKCHAIN')
        except:
            time.sleep(5)
            continue
        L = int(s.recv(1024).decode())
        bc = Rigs.BlockChain()
        data = bc.Load()
        if(L > len(data)):
            print('[*] Found Larger BlockChain')
            s.send(b'CONTINUE')
            end = b''
            data = s.recv(1024)
            end += data
            while data.decode()[-3:] != 'EOF':
                data = s.recv(1024)
                end += data
            if(end[-3:] == b'EOF'):
                end = end[:-3]
            bc.blockchain = ast.literal_eval(end.decode())
            if(bc.Verify()):
                bc.SaveWhole()
                print('[+] New BlockChain Saved')
            else:
                print('[-] New BlockChain Invalid. Discarded')
        else:
            s.send(b' ')
        time.sleep(60)


t = Thread(target=CheckBlockChain)
t.start()



#wallet_folder = 'Keys/'+os.listdir('Keys')[0]
#key = Rigs.Key()
#key.Load(wallet_folder)
Window()
