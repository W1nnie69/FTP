import re
import socket
import tqdm
import os
import tkinter as tk


buffer_size = 4096

separator = "<SEPARATOR>"


def receivergui():
    receiverroot = tk.Tk()
    receiverroot.title("The better Google drive")

    canvas1 = tk.Canvas(receiverroot, width=800, height=700)
    canvas1.pack()

    img1 = tk.PhotoImage(file="sussy.gif")
    canvas1.create_image(233, 344, image=img1)

    receiverroot.mainloop()


def startserver():
    myip = "0.0.0.0"
    myport = int(input("Please enter the port you are using(Leave empty for default port 6969): ") or 6969)
    print(myip)
    print(myport)
    s = socket.socket()
    s.bind((myip, myport))
    s.listen(5)
    print(f"[*] Listening as {myip}:{myport}")
    client_socket, address = s.accept()
    print(f"[+] {address} is connected.")
    received = client_socket.recv(buffer_size).decode()
    filename, filesize = received.split(separator)
    filename = os.path.basename(filename)
    filesize = int(filesize)


    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        while True:
            bytes_read = client_socket.recv(buffer_size)

            if not bytes_read:
                break

            f.write(bytes_read)
            progress.update(len(bytes_read))

    client_socket.close()
    s.close()


startserver()