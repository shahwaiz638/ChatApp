import tkinter as tk
from tkinter import *
from tkinter import messagebox
import socket
import threading
import json

host = '192.168.0.1'
port = 12334
username = None
connectedOrNot = False
registered = False
msg = None
text = None
symmetric=True

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def encrypt(plaintext, key):
    # Generate a random 128-bit (16-byte) IV (Initialization Vector)
    iv = os.urandom(16)

    # Create an AES cipher with the key and IV
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    encryptor = cipher.encryptor()

    # Encrypt the plaintext
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    # Return the IV and ciphertext
    return iv + ciphertext

def decrypt(ciphertext, key):
    # Split the IV and ciphertext
    iv = ciphertext[:16]
    ciphertext = ciphertext[16:]

    # Create an AES cipher with the key and IV
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    decryptor = cipher.decryptor()

    # Decrypt the ciphertext
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    return plaintext

def onClosing():
    if messagebox.askokcancel("Quit", "Do you want to quit or not?"):
        root.destroy()


def serverConnect():
    global connectedOrNot
    if(not connectedOrNot):
        try:
            c.connect((host, port))
            print("Connected to the chat room")
            label = tk.Label(frame, text= "Connected to the chat room",fg= "#ADD8E6", bg= "#263D42")
            label.pack()
            connectedOrNot = True
        except:
            for wid in frame.winfo_children():
                wid.destroy()
            print("Room Unavailable")
            label = tk.Label(frame, text= "Room Unavailable",fg= "#263D42", bg= "#ADD8E6")
            label.pack()

def setUsername():
    global msg,text
    if(connectedOrNot):
        Label(frame, text='Username', pady=10, fg= "#ADD8E6", bg='#263D42').pack()

        e = Entry(frame, width= 35, bg= "#ADD8E6")
        e.pack()
        e.insert(0, "")
        Done = tk.Button(frame, text= "Done", padx= 9, pady= 6, fg= "#ADD8E6", bg= "#263D42", command= lambda:FixUsername(e))
        Done.pack()
        ############################################
        Label(frame, text='Message', pady=10, fg= "#ADD8E6", bg='#263D42').pack()
        msg = Entry(frame, width=70, bg="#ADD8E6")
        msg.pack()
        msg.insert(0, "")
        Done = tk.Button(frame, text= "Send", padx= 9, pady= 6, fg= "#ADD8E6", bg= "#263D42", command= lambda:sendButton())
        Done.pack()

        text = Text(frame,width = 45, height = 10,padx = 5,   pady = 5, fg ="#263D42" , bg="#ADD8E6")
        
        text.place(relheight = 0.745,            relwidth = 1,     rely = 0.08)

        text.config(cursor = "arrow")

        text.config(state=DISABLED)
        text.pack()

        StartRecv = tk.Button(frame, text= "Enable", padx= 25, pady= 20, fg= "#ADD8E6", bg= "#263D42", command= lambda:StartRecieving())
        StartRecv.pack()
        #text = Label(Frame, text = "Empty", height= 10, width=20).pack()


    else:
        for wid in frame.winfo_children():
                wid.destroy()
        label = tk.Label(frame, text= "Unable to connect to the Server",fg= "#263D42", bg= "#ADD8E6")
        label.pack()

def FixUsername(e):
    global username
    global registered
    e.config(state="disabled")
    p_key=8
    username = str(e.get())
    connection_msg=[username,p_key]
    # Convert the list to a JSON string
    connection_msg_json = json.dumps(connection_msg)

    # Encode the JSON string to bytes
    connection_msg_bytes = connection_msg_json.encode()
    c.send(connection_msg_bytes)
    print("Client setting username: ",username)
    Label(frame, text=f'{username}, Registered!', pady=10, fg= "#ADD8E6", bg='#263D42').pack()
    Label(frame, pady=10, fg= "#ADD8E6", bg='#263D42').pack()
    registered = True


def sendButton():
    if(registered):
        Send = threading.Thread(target= send, args= (c,) )
        Send.start()

def send(c):
    #while True:
    message = username + ':' + msg.get()
    message=encrypt(message, key)
    print("Client: ",message)
    c.send(message.encode())
        
def StartRecieving():
    if(registered):
        Recieve = threading.Thread(target= recieve, args= (c,) )
        Recieve.start()
        


def recieve(c):
    global text
    key_exchange = True
    while True:
        try:
            if(key_exchange==False):
                c.send(8)
                print("app sent private key")
                message = c.recv(2048).decode()
                print("app recived shared key")
                key_exchange=True

            message = c.recv(2048).decode()
            print("recived from server: ",message)
            text.config(state = NORMAL)
            text.insert(END,message+"\n\n")
            text.config(state = DISABLED)
            text.see(END)

            print(message)
        except:
            c.close()
            break




###GUI
root = tk.Tk()


canvas = tk.Canvas(root, height=600, width=  600, bg = "#ADD8E6")
canvas.pack()


frame = tk.Frame(root, bg = "#263D42")
frame.place(relwidth=0.8, relheight= 0.7, relx= 0.1, rely= 0.1)

connectButton = tk.Button(root, text= "Connect to the Room", padx= 11, pady= 6, fg= "#ADD8E6", bg= "#263D42", command= lambda:serverConnect())
connectButton.pack()


addUsername = tk.Button(root, text= "Add Username", padx= 11, pady= 6, fg= "#ADD8E6", bg= "#263D42", command= lambda:setUsername())
addUsername.pack()

root.protocol("WM_DELETE_WINDOW", onClosing)
root.mainloop()

###Func





    