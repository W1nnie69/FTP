import time, socket, os ,tqdm, json
import customtkinter as ctk
from PIL import Image
import tkinter as tk
import threading










class FTPApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        global size
        size = "900x500"

        self.geometry(size)
        self.title("FTP")

        # self.grid_rowconfigure(0, weight=1)  # configure grid system
        # self.grid_columnconfigure(0, weight=1)
        
        self._frame = None
        self.switch_frames(mainframe)


        
        # mainframe = ctk.CTkFrame(self)
        # mainframe.grid_rowconfigure(0, weight=1)
        # mainframe.grid_columnconfigure(0, weight=1)
        # mfsenderbutton = ctk.CTkButton(master=mainframe, text="Send file") 
        # mfsenderbutton.grid(row=1, column=1, sticky="nsew")



        # senderframe = ctk.CTkFrame(self)
        # receiverframe = ctk.CTkFrame(self)

        # self.show_frame(mainframe)

    def switch_frames(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid(row=0,column=0)
        

        











class mainframe(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.configure(fg_color="#242424")
        
        # self.grid_rowconfigure(0, weight=1)
        # self.grid_columnconfigure(0, weight=1)

        self.senderbutton = ctk.CTkButton(self, width=150, height=80, text="Send file", command=lambda: master.switch_frames(senderframe))
        self.senderbutton.grid(row=0, column=0, padx=(280,25), pady=(120,120))

        

        self.receiverbutton = ctk.CTkButton(self, width=150, height=80, text="Receive file")
        self.receiverbutton.grid(row=0, column=1, padx=(1,1))

    def removeframe(self):
        self.grid_forget()
        FTPApp.gotosenderframe(self)












    
class ToplevelWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.geometry("400x350")





        self.nameentry = ctk.CTkEntry(self, placeholder_text="Name goes here")
        self.ipentry = ctk.CTkEntry(self, placeholder_text="Ip goes here")
        self.savebutton = ctk.CTkButton(self, text="save", width=30, command=lambda: self.updatejson())

        self.nameentry.grid(row=0, column=0)
        self.ipentry.grid(row=1, column=0)
        self.savebutton.grid(row=0, column=1)






    def write_json(self, new_data, filename='mydata.json'):
        with open(filename,'r+') as file:
            # First we load existing data into a dict.
            file_data = json.load(file)
            # Join new_data with file_data inside emp_details
            file_data["address"].append(new_data)
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(file_data, file, indent = 4)




    def updatejson(self):
        with open("mydata.json", "r") as f:
                data = json.load(f)

        name = self.nameentry.get()
        ip = self.ipentry.get()
        
        newlist ={
                    
                        "name":name,
                        "ip":ip,
                        "id":str(len(data["address"])+1)
                    
                    }

        print(newlist)

        self.write_json(newlist)
        self.destroy()











class senderframe(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.configure(fg_color="#242424")
    
               
        # self.grid_rowconfigure(1, weight=0)
        # self.grid_columnconfigure(0, weight=0)

        
        
        self.stop_flag = threading.Event()


        self.selectfilebutton = ctk.CTkButton(self, width=100, height=50, text="Select a file to send", command=lambda: self.getfilepath())
        
        self.selectfilebutton.grid(row=0, column=0 ,pady=(100,0), padx=(15,0))


        self.label = ctk.CTkLabel(self, text="Select the receiver:")
        self.label.grid(row=1, column=0, padx=(10,0), pady=(25,))

        names = self.getname()
        
        self.addroptions = ctk.CTkOptionMenu(self, values=names)
        self.addroptions.grid(row=2, column=0, padx=(22,0), pady=(0,0))

        
        self.setbutton = ctk.CTkButton(self, text="set", width=40, height=30, command=lambda: self.setreceiverinfo())
        self.setbutton.grid(row=2, column=1, padx=(10,0), pady=(0,0))

        self.add_new_receiver = ctk.CTkButton(self, text="add", width=40, height=30, command=lambda: self.add())
        self.add_new_receiver.grid(row=2, column=2, padx=(10,0), pady=(0,0))

        self.sendbutton = ctk.CTkButton(self, text="Send the file :)", width=150, height=70, command=lambda: self.start_sendfile_thread())
        self.sendbutton.grid(row=3, column=0, padx=(30,0), pady=(40,0))

        self.toplevel_window = None

    

    def getfilepath(self):
        clientroot = tk.Tk()
        clientroot.withdraw()
        global filename
        global filesize
        filename = []
        filesize = []
        fn = tk.filedialog.askopenfilename()
        clientroot.destroy()
        fs = os.path.getsize(fn)
        filename.append(fn)
        filesize.append(fs)
        print(filename, filesize)
        

        file = f"File {filename} is selected"
        self.filename = ctk.CTkLabel(self, text=file)
        self.filename.grid(row=0,column=1,pady=(90,0),padx=(10,0), columnspan=1000)



    def getname(self):
        with open('mydata.json', 'r') as f:
            data = json.load(f)

        addresses = data["address"]

        address_names = [address["name"] for address in addresses]

        return address_names







    def on_option_changed(self):
        print("Selected address:", self.addroptions.get())
    






    def setreceiverinfo(self):
        global selected
        global ip
        selected = self.addroptions.get()
        print(selected)  

        with open('mydata.json', 'r') as f:
            data = json.load(f)

        ip = []

        for address in data["address"]:
            if address['name'] == selected:
                getip = address['ip']
                
                ip.append(str(getip))
                break
        
        
        else:
            print("error")

        
    




    def start_sendfile_thread(self):
        print('starting thread')
        self.thread1 = threading.Thread(target=self.sendfile)
        self.thread1.start()

        self.sendbutton.configure(state="disabled")
        self.after(100, self.update_progress_bar)


    def stop_sendfile_thread(self):
        self.stop_flag.set()
        self.thread1.join()

        print("worker has stopped")





    def sendfile(self):
        print(ip)
        print("")

        self.progressbar = ctk.CTkProgressBar(self, mode="determinate")
        self.progressbar.grid(row=4, column=0, padx=(20,0), pady=(20,0))
        self.progressbar.set(0)

        realip = ip[0]

        separator = "<SEPARATOR>"
        buffer_size = 4096

        port = 6969

        print(f"[+] Connecting to {realip}:{port}")
        s = socket.socket()

        try:
            s.connect((realip,port))
            s.send(f"{filename}{separator}{filesize}".encode())


        except TimeoutError as e:
            print(f'Error connecting to {realip}:{port}: {e}')   
            self.stop_flag.set()
            self.sendbutton.configure(state="normal")
            self.progressbar.destroy()
            raise
            

        else:
             print(f'Successfully connected to {realip}:{port}')    

        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)

        with open(filename, "rb") as f:
            while True:
            
                bytes_read = f.read(buffer_size)
                if not bytes_read:
                    break
            
                s.sendall(bytes_read)
                progress.update(len(bytes_read))
                

                
                
        s.close()

        print("done")

        self.stop_flag.set()

        self.sendbutton.configure(state="normal")
        self.progressbar.destroy()








    def add(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self)# create window if its None or destroyed
            self.toplevel_window.focus()  
        else:
            self.toplevel_window.focus()  # if window exists focus it













class receiverframe(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.configure(fg_color="#242424")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)





















    

if __name__ == "__main__":

    app = FTPApp()
    app.mainloop()






















