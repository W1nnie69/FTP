import client
import server
import tqdm
import time
from tkinter import *

    

def startup():
    print("Welcome to My FTP")
    time.sleep(1)
    input1 = input("Please select if you would like to receive or send (R/S) ")
    while True:
        if input1 == "S":
            print("Please select the file you would like to send")
            client.getfilepath()
            client.connecttoserver()

            confirm = input("Send the file? Y/N(Type N to reselect file) ")

            loop = True

            while loop == True:
                if confirm == "Y":
                    loop = False
                    client.send()
                    print("ok file done sending")
                    time.sleep(1)
                 
                elif confirm == "N":
                    loop = False
                    client.getfilepath()
                    confirm = input("Send the file? Y/N  ")

                else:
                    print("Input invalid idiot, its either a yes or a no")
                    time.sleep(1)
                    confirm = input("Send the file? Y/N  ")

            




        elif input1 == "R":
            server.startserver()
            print("Download is done!")
            time.sleep(5)
            quit()
            

        else:
            input1 = input("Please select if you would like to receive or send (R/S) ")
            



if __name__ == '__main__':
    startup()




