import socket
import pymysql
import random
import time
from threading import Thread

HTTP_SUCCESS = """HTTP/1.1 200 OK

"""


def now_time():
    tiem_ = time.ctime()
    return tiem_.encode()


def rand_num():
    num = random.randint(1, 24)
    return num


db = pymysql.connect(host="127.0.0.1",
                     port=3306,
                     user="root",
                     password="csy123,",
                     database="grade", )
cur = db.cursor()

sockfd = socket.socket(socket.AF_INET,
                       socket.SOCK_STREAM)
sockfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock_network = ("0.0.0.0", 80)
sockfd.bind(sock_network)
sockfd.listen(100)


def put_image():
    print("Connect listen is...")
    conn, addr = sockfd.accept()
    nowtime = now_time()
    with open("./addr.log", "ab+") as addr_file:
        addr_file.write(str(addr).encode() + " ".encode() + nowtime)
        addr_file.write("\n".encode())

    data = conn.recv(204800)
    print(data.decode())
    if not data:
        conn.close()
        return

    resu_num = rand_num()
    if resu_num < 19:
        sql_insert = "SELECT image FROM yuanshen_image WHERE id=%s" % resu_num
    else:
        second_num = resu_num - 18
        sql_insert = "SELECT image FROM mao_image WHERE id=%s" % second_num
    cur.execute(sql_insert)
    image_result = cur.fetchall()[0][0]

    second_data = data.decode().split(" ")[1]
    if second_data == "/favicon.ico":
        conn.send(b"")
        conn.close()
        return
    missage = HTTP_SUCCESS.encode() + image_result
    conn.send(missage)


while True:
    th = Thread(target=put_image)
    th.setDaemon(True)
    th.start()
    th.join()
