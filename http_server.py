"""
http_server
"""
import socket
from select import select


class HttpServer:
    def __init__(self, host="0.0.0.0", post=80):
        self.__post = post
        self.__addr = (host, int(post))
        self.__creat_sockfd()
        self.__rlist = [self.__sockfd]

    # http200响应头
    def __http_200_head(self, dir, connfd):
        head = """HTTP/1.1 200 OK

        """
        try:
            content = self.__select_file(dir)
            result = head.encode() + content
            connfd.send(result)
        except Exception as e:
            print(e)
            self.__http_400_head(connfd)

    # http400响应头
    def __http_400_head(self, connfd):
        head = """HTTP/1.1 404 Not Found

        <h1>404</h1>
        """
        connfd.send(head.encode())

    # 读取网页内容
    def __select_file(self, dir):
        with open(dir, "rb") as f:
            content = f.read()
        return content

    # 创建套接字
    def __creat_sockfd(self):
        self.__sockfd = socket.socket()
        self.__sockfd.setsockopt(socket.SOL_SOCKET,
                                 socket.SO_REUSEADDR, 1)
        self.__sockfd.bind(self.__addr)

    # 启动服务
    def server_forever(self):
        self.__sockfd.listen(5)
        print("Listen the post %d" % self.__post)
        self.__IO_start()

    # IO多路复用
    def __IO_start(self):
        while True:
            rs, ws, zs = select(self.__rlist, [], [])
            for item in rs:
                if item is self.__sockfd:
                    self.__sockfd_run(item)
                else:
                    self.__connfd_run(item)

    # sockfd执行
    def __sockfd_run(self, sockfd):
        connfd, addr = sockfd.accept()
        print("Connect from %s" % str(addr))
        self.__rlist.append(connfd)

    # http协议处理
    def __http_message(self, data):
        head = data.split(" ")[0]
        body = data.split(" ")[1]
        if head == "POST":
            result_data = data.split("\r\n")[-1]
            return (head, body, result_data)
        return (head, body)

    # connfd执行
    def __connfd_run(self, connfd):
        data = connfd.recv(10240)
        print(data.decode())
        try:
            get_content = self.__http_message(data.decode())
        except IndexError as e:
            return
        print(get_content)
        if not data:
            connfd.close()
            self.__rlist.remove(connfd)
        if get_content[1] == "/":
            self.__http_200_head("./index.html", connfd)
        elif get_content[1][-5:] == ".html":
            html_dir = "." + get_content[1]
            self.__http_200_head(html_dir, connfd)
        else:
            self.__http_400_head(connfd)
        self.__rlist.remove(connfd)
        connfd.close()


if __name__ == "__main__":
    httpserver = HttpServer()
    httpserver.server_forever()
