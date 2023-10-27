import socket
import threading
import time
import pickle
import deffy_hellman as df
import json

host = socket.gethostbyname(socket.gethostname())
port = 12334

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))

clientle = {}

s.listen()





def clientThread(conn):
    while True:
        try:
            message = conn.recv(2048)
            for client in clientle:
                client.send(message)
                print("server: ",message)
        except:
            conn.close()
            del clientle[conn]
            for client in clientle:
                if client != conn:
                    message = username + ' has left the room'
                    client.send(message.encode())
                    print("server: ",message)
            break


keys=[]
while True:
    print('Waiting For Users')
    conn, addr = s.accept()
    print('Chat Room Active')
    received_data = conn.recv(2048).decode()

    # Decode the received JSON string
    connection_msg = json.loads(received_data)

    # Extract the username and keys
    username = connection_msg[0]
    keys.append(connection_msg[1])
    clientle[conn] = username
    print(clientle)
    print(keys)

    if(len(clientle)==2):
        print(" there are clients in the room")
        
        # p1=conn.recv(2048).decode()
        # print("key1 recv")
        # p2=conn.recv(2048).decode()
        # print("key2 recv")

        shared_key=df.deffy_hellman(keys[0],keys[1])

        print("the shared key is: ", shared_key)
        for client in clientle:
            if client != conn:
                message = [username + ' has entered the room']
                message.append(shared_key)
                client.send(message.encode())
                print("server: ",message)

    threading.Thread(target = clientThread, args= (conn, )).start()
