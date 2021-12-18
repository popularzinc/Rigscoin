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

SERVER_IP = '192.168.1.14'
PORT = 3000

class Window:
    def __init__(self,key=Rigs.Key()):
        self.key = key

        root = tk.Tk()
        root.title("Tab Widget")
        root.geometry('700x500+700+200')

        tabControl = ttk.Notebook(root)

        tab1 = ttk.Frame(tabControl)
        tab2 = ttk.Frame(tabControl)
        self.tab3 = ttk.Frame(tabControl)

        tabControl.add(tab1, text='Home')
        tabControl.add(tab2, text='Send')
        tabControl.add(self.tab3, text='Addresses')

        tabControl.pack(expand=True, fill="both")

        self.ListAddresses()

        T = ttk.Label(tab1, text="Address",foreground='grey')#.grid(column=0, row=0, padx=30, pady=30)
        T.pack(side=TOP,padx=5,pady=5)

        self.Address = ttk.Label(tab1, text=self.key.address,font='bold')#.grid(column=0, row=0, padx=30, pady=30)
        self.Address.pack(side=TOP,padx=5,pady=5)

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
        for i in os.listdir('Keys'):
            f = open('Keys/'+str(i)+'/address','r')
            data = f.read()
            f.close()
            T = ttk.Label(self.tab3, text=str(i)+': '+str(data))#.grid(column=0, row=0, padx=30, pady=30)
            T.pack(side=TOP,padx=5,pady=5)
            B = ttk.Button(self.tab3, text="Select", command = lambda x=i: self.select(x))
            B.pack(side=TOP,padx=5,pady=5)
        B = ttk.Button(self.tab3, text="Create New Address", command = self.Create)
        B.pack(side=TOP,padx=5,pady=5)

    def Create(self):
        new_key = Rigs.Key()
        new_key.Generate()
        new_key.Save('Keys/'+Random())
        self.ListAddresses()

    def select(self,n):
        new_key = Rigs.Key()
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

def CheckBlockChain():
    print('Hello')
    while True:
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
