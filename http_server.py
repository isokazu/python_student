import socket
import time
from select import select

with open("./index.html", "rb") as f:
    index = f.read()


def request(connfd):
    msg = connfd.recv(10240).decode()
    try:
        line = msg.split(" ")[1]
    except IndexError:
        line = "/"
    return line


def new_time():
    new_time = time.ctime()
    return new_time


def message(get):
    now_time = new_time().encode()
    if get == "/":
        response = """HTTP/1.1 200 OK

        """
        response = response.encode() + index + now_time
        return response
    else:
        response = """HTTP/1.1 404 Not Found
        
        <h1>404</h1>
        """
        return response.encode()


sockfd = socket.socket()
sockfd.setsockopt(socket.SOL_SOCKET,
                  socket.SO_REUSEADDR, 1)
sockfd.bind(("0.0.0.0", 9998))
sockfd.listen(5)

rlist = [sockfd]
while True:
    rs, ws, xs = select(rlist, [], [])
    for item in rs:
        if item is sockfd:
            c, addr = item.accept()
            print("Connect from ", str(addr))
            rlist.append(c)
        else:
            req = request(item)
            response = message(req)
            item.send(response)
            rlist.remove(item)
            item.close()

