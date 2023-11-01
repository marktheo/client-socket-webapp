# Importing necessary libraries
from flask import Flask, request, render_template
import socket as sckt
import threading, os

# Flask instance
app = Flask(__name__)

# Getting process ID for later kill
own_pid = os.getpid()

# Server IP and port
server_addr = ('', 18000)

# Client socket instance (TCP)
client_sckt = sckt.socket(sckt.AF_INET, sckt.SOCK_STREAM)
# Client connection attempt
client_sckt.connect(server_addr)

# Message transmission function
def transmit(string):
    msg = string.encode('utf-8')
    msg_len = str(len(msg)).encode('utf-8')
    msg_len += b' ' * (64 - len(msg_len))
    client_sckt.send(msg_len)
    client_sckt.send(msg)

# Message listening function
def listen():
    while True:
        string = client_sckt.recv(2048).decode('utf-8')
        if not string:
            break
        print("\n" + string)

# Main page
@app.route("/")
def page():
    return render_template("chat.html")

# Main page formulary post method
@app.route("/chat", methods=["POST"])
def chat():
    message = request.form["message"]
    transmit(message)
    if message == ":D":
        client_sckt.close()
        global own_pid
        os.kill(own_pid, 9)
    return page()

# Application threading and beginning
if __name__ == "__main__":
    server = threading.Thread(target=listen)
    server.daemon = True
    server.start()
    app.run()