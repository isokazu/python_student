"""
dict 客户端
功能： 根据用户输入，发送请求，得到结果
"""
from getpass import getpass
import sys
import socket

first = """
==============Welcome===============
 1. 注册       2. 登录        3. 退出
====================================
"""

second = """
==============Welcome===============
 1. 查单词    2. 历史记录       3. 注销
====================================
"""


# 用户注册
def register(sockfd):
    USER = input("请输入用户名>>")
    PASSWD = getpass("请输入密码>>")
    CONFIRM = getpass("请再次输入密码>>")
    if PASSWD != CONFIRM:
        ret = "两次密码不一致"
        return ret
    result = "REGISTER_AGREEMENT\nUSER: %s\nPASSWD: %s" % (USER, PASSWD)
    sockfd.send(result.encode())
    data = sockfd.recv(10240)
    return data.decode()


# 用户登录
def sign_in(sockfd):
    USER = input("请输入用户名>>")
    PASSWD = getpass("请输入密码>>")
    result = "SIGN_IN_AGREEMENT\nUSER: %s\nPASSWD: %s" % (USER, PASSWD)
    sockfd.send(result.encode())
    data = sockfd.recv(10240)
    return data.decode()


# 用户退出
def client_exit(sockfd):
    message = "*DICT_USER_EXIT*\n"
    sockfd.send(message.encode())
    sockfd.close()
    sys.exit("程序已退出")


# 查单词
def select_word(sockfd, user_name):
    WORD = input("请输入单词>>")
    result = "CLIENT_WORD\n%s\n%s" % (str(user_name), WORD)
    sockfd.send(result.encode())
    data = sockfd.recv(10240)
    return data.decode()


# 历史记录
def select_history(sockfd, user_name):
    result = "CLIENT_HISTORY\n%s" % str(user_name)
    sockfd.send(result.encode())
    data = sockfd.recv(102400)
    return data.decode()


def main():
    sockfd = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM)
    sockfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ADDR = ("81.70.133.161", 8001)
    sockfd.connect(ADDR)
    while True:
        print(first)
        cmd = input("输入选项：")
        reg = 0
        sig = 0
        user_name = None
        if cmd == "1":
            reg_old = register(sockfd)
            try:
                reg = reg_old.split("\n")[0]
                user_name = reg_old.split("\n")[1]
            except IndexError:
                reg = reg_old
            except Exception as e:
                continue
        elif cmd == "2":
            sig_old = sign_in(sockfd)
            try:
                sig = sig_old.split("\n")[0]
                user_name = sig_old.split("\n")[1]
            except IndexError:
                sig = sig_old
            except Exception as e:
                continue
        elif cmd == "3":
            client_exit(sockfd)
        else:
            print("没有此选项，请重新输入")
            continue
        if reg == "register_success" or sig == "sign_in_success":
            while True:
                print(second)
                cmd_two = input("输入选项：")
                if cmd_two == "1":
                    word = select_word(sockfd, user_name)
                    print(word)
                elif cmd_two == "2":
                    his = select_history(sockfd, user_name)
                    print(his)
                elif cmd_two == "3":
                    break
                else:
                    print("没有此选项，请重新输入")
                    continue
        else:
            if reg:
                print(reg)
            elif sig:
                print(sig)


if __name__ == "__main__":
    main()
