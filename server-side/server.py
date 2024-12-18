import socket
from threading import Thread

host = "localhost"
port = 8080

clients = {}  

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((host, port))


def handle_clients(conn):

    name = conn.recv(1024).decode()

    welcome = f"Welcome {name}.)"
    conn.send(bytes(welcome, "utf8"))

    msg = name + " has recently joined us"

    broadcast(bytes(msg, "utf8"))

    clients[conn] = name

    while True:
        msg = conn.recv(1024)
        broadcast(msg, name + ":")

def broadcast(msg, prefix=""):
    for client in clients:  
        client.send(bytes(prefix, "utf8") + msg)


def accept_client_connection():
    while True: 
        client_conn, client_address = sock.accept()  
        print(client_address, " has Connected")

        client_conn.send(bytes("Welcome to the chat room, Please type your name to continue", "utf8"))

        Thread(target=handle_clients, args=(client_conn,)).start()


if __name__ == "__main__":
    print("Starting server....Accepting up to 3 connections")
    sock.listen(3)  
    print("listening on port : ", port, "......")


    t = Thread(target=accept_client_connection)

    t.start()  
    t.join()  