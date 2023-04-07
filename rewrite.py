import time, socket, os ,tqdm, json
import customtkinter as ctk
from PIL import Image
import tkinter as tk


class FTPApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        global size
        size = "900x700"

        self.geometry(size)
        self.title("FTP")

        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)
        
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
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.senderbutton = ctk.CTkButton(self, width=150, height=80, text="Send file", command=lambda: master.switch_frames(senderframe))
        self.senderbutton.grid(row=0, column=0, padx=10, sticky="nsew")
        
        self.receiverbutton = ctk.CTkButton(self, width=150, height=80, text="Receive file")
        self.receiverbutton.grid(row=0, column=1, padx=10, sticky="nsew")

    def removeframe(self):
        self.grid_forget()
        FTPApp.gotosenderframe(self)




class senderframe(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.configure(fg_color="#242424")
        
        
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(1, weight=0)

        
        

        self.selectfilebutton = ctk.CTkButton(self, width=100, height=50, text="Select a file to send", command=lambda: self.getfilepath())
        
        self.selectfilebutton.grid(row=1, column=1, sticky="nsew")

        # self.filename = ctk.CTkLabel(self, text=file, pady=20)
        # self.filename.grid(row=2,column=1,sticky="nsew")
        


    def getfilepath(self):
        clientroot = tk.Tk()
        clientroot.withdraw()
        global filename
        global filesize
        filename = tk.filedialog.askopenfilename()
        clientroot.destroy()
        filesize = os.path.getsize(filename)
        print(filename)
        file = f"File {filename} is selected"
        self.filename = ctk.CTkLabel(self, text=file)
        self.filename.grid(row=2,column=1,sticky="nsew")




class receiverframe(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.configure(fg_color="#242424")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)






















    

if __name__ == "__main__":

    app = FTPApp()
    app.mainloop()






















