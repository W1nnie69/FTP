from inspect import getfile
from itertools import tee
import socket
import os
import tqdm
import tkinter as tk
from tkinter import filedialog
import json


#ipaddressbook = {}
#ipaddressbook = {'address': {'name':'defualt', 'ip':'0.0.0.0', 'id':1}}



separator = "<SEPARATOR>"

buffer_size = 4096



def write_json(new_data, filename='mydata.json'):
    with open(filename,'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["address"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)







def getfilepath():
    clientroot = tk.Tk()
    clientroot.withdraw()
    global filename
    global filesize
    filename = tk.filedialog.askopenfilename()
    clientroot.destroy()
    filesize = os.path.getsize(filename)
    print(filename)
    



def connecttoserver():
    global s
    global ipaddressbook

    ipaddressbook = {"address":[{"name":"test", "ip":"0.0.0.0","id":"1"}]} 
    
    


    qn = input("Use a saved ip address? (Y/N/Manual)"  )

    check = True

    while check is True:
        if qn == "Y":
            check = False
            
            with open("mydata.json", "r") as f:
                ipaddressbook = json.load(f)

        
            number = len(ipaddressbook["address"])
        

            for x in range(number):
                name = ipaddressbook["address"][x]["name"]
                ipname = ipaddressbook["address"][x]["ip"]
                idname = ipaddressbook["address"][x]["id"]
            
                print(idname,name,ipname,)
            

        

            ans = int(input(""))
            ip = ipaddressbook["address"][ans - 1]["ip"]

        
        
            print("Ip address", ip, "selected")
    


        elif qn == "N":
            check = False

            with open("mydata.json", "r") as f:
                ipaddressbook = json.load(f)

            ip = input("Please enter the receiver's ip address= ")
            name = input("Please enter the receiver's name= ")
    
            newlist ={
                    
                        "name":name,
                        "ip":ip,
                        "id":str(len(ipaddressbook["address"])+1)
                    
                    }
                
        
        
            write_json(newlist)

                
        elif qn == "Manual":
            check = False
            ip = input("Please enter the receiver's ip address= ")

        
        

        else:
            check = True
            qn = input("Use a saved ip address? (Y/N)"  )
        
        
    
    
    port = input("Please enter the port you are using(Leave empty for default port 6969): ") or 6969
    p = int(port)
    print(f"[+] Connecting to {ip}:{port}")
    s =  socket.socket()
    s.connect((ip, p))
    s.send(f"{filename}{separator}{filesize}".encode())
    



def send():
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)

    with open(filename, "rb") as f:
        while True:
        
            bytes_read = f.read(buffer_size)
            if not bytes_read:
                break
        
            s.sendall(bytes_read)
       
            progress.update(len(bytes_read))
            
    s.close()
    




def testfn():
    print("something")

