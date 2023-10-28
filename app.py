from flask import Flask, request, render_template
import socket as sckt
import os

#Flask Instance - Init
app = Flask(__name__)
own_pid = os.getpid()

server_addr = ('127.0.0.101', 18000)

client_sckt = sckt.socket(sckt.AF_INET, sckt.SOCK_STREAM)
client_sckt.connect(server_addr)

def go(string):
    msg = string.encode('utf-8')
    msg_len = str(len(msg)).encode('utf-8')
    msg_len += b' ' * (64 - len(msg_len))
    client_sckt.send(msg_len)
    client_sckt.send(msg)
    print(client_sckt.recv(2048).decode('utf-8'))

@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route("/send", methods = ["POST"])
def send():
    message = request.form["message"]
    if message == ":D":
        client_sckt.close()
        global own_pid
        os.kill(own_pid, 9)
    else:
        go(message)
    return chat()

app.run()