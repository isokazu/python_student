"""
字典查询系统
用户注册，用户登陆，查询单词，查询历史记录，客户退出登录
"""
import socket
import hashlib
import signal
import sys
import re
from mysql_continul import DoDatabase
from multiprocessing import Process

# 不接收子进程信号，用于处理僵尸进程
signal.signal(signal.SIGCHLD, signal.SIG_IGN)

# 创建数据库
do_data = DoDatabase()


# 哈希加密
def hash_passwd(passwd):
    # 生成md5加密方法的hash对象(加盐处理)
    hash = hashlib.md5("0#xIl_/3*".encode())
    # 使用hash对象进行加密(传入字节串)
    hash.update(passwd.encode())
    # 获取加密后的密码
    hash_pwd = hash.hexdigest()
    return hash_pwd


# 用户注册
def server_register(conn, message, cul):
    try:
        result = message.split("\n")
        USER = re.findall("USER: (.*)", result[1])[0]
        PASSWD = re.findall("PASSWD: (.*)", result[2])[0]
    except Exception as e:
        conn.send("NO".encode())
        print(e)
        return
    have_user = do_data.user_in_database(USER, cul)
    if not have_user:
        PWD = hash_passwd(PASSWD)
        insert_success = do_data.insert_user(USER, PWD, cul)
        if insert_success == "insert ok":
            ret_mes = "register_success\n%s" % USER
            conn.send(ret_mes.encode())
        else:
            ret_mes = "注册失败"
            conn.send(ret_mes.encode())
    else:
        ret_mes = "用户名已存在"
        conn.send(ret_mes.encode())


# 用户登陆
def server_land(conn, message, cul):
    try:
        result = message.split("\n")
        USER = re.findall("USER: (.*)", result[1])[0]
        PASSWD = re.findall("PASSWD: (.*)", result[2])[0]
    except Exception as e:
        conn.send("NO".encode())
        print(e)
        return
    PWD = hash_passwd(PASSWD)
    have_user = do_data.user_in_database(USER, cul)
    if not have_user:
        ret_mes = "用户名不存在"
        conn.send(ret_mes.encode())
    elif have_user[0] != PWD:
        ret_mes = "密码不正确"
        conn.send(ret_mes.encode())
    else:
        ret_mes = "sign_in_success\n%s" % USER
        conn.send(ret_mes.encode())


# 查单词
def server_word(conn, message, cul):
    user_name = message.split("\n")[1]
    user_word = message.split("\n")[2]
    do_data.insert_history(user_name, user_word, cul)
    ret_word = do_data.select_word(user_word, cul)
    if not ret_word:
        ret_msg = "没有找到此单词"
        conn.send(ret_msg.encode())
    else:
        ret_msg = "%s : %s" % (ret_word[0], ret_word[1])
        conn.send(ret_msg.encode())


# 查询历史记录
def server_history(conn, data, cul):
    user_name = data.split("\n")[1]
    word = do_data.select_history(user_name, cul)
    if not word:
        res_msg = "没有历史记录"
        conn.send(res_msg.encode())
    else:
        res_msg = "%s" % word
        conn.send(res_msg.encode())


# 客户端数据处理
def request(conn):
    cul = do_data.create_cul()
    while True:
        data = conn.recv(10240).decode()
        if not data:
            conn.close()
            do_data.delete_cul(cul)
            return
        HEAD = data.split("\n")[0]
        if HEAD == "*DICT_USER_EXIT*":  # 客户端退出
            conn.close()
            do_data.delete_cul(cul)
            return
        elif HEAD == "REGISTER_AGREEMENT":  # 注册
            server_register(conn, data, cul)
        elif HEAD == "SIGN_IN_AGREEMENT":  # 登陆
            server_land(conn, data, cul)
        elif HEAD == "CLIENT_WORD":  # 查单词
            server_word(conn, data, cul)
        elif HEAD == "CLIENT_HISTORY":  # 历史记录
            server_history(conn, data, cul)


def main():
    # 创建服务端套接字
    sockfd = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM)
    sockfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ADDR = ("0.0.0.0", 8001)
    sockfd.bind(ADDR)
    sockfd.listen(100)
    print("Listen the port 8001")
    # 循环等待客户端连接
    while True:
        try:
            conn, addr = sockfd.accept()
            print("Connect from the ", addr)
        except KeyboardInterrupt:
            sockfd.close()
            sys.exit("服务端退出")
        except Exception as e:
            print(e)
            continue

        # 创建子进程用于处理客户端请求
        pro = Process(target=request, args=(conn,))
        # 进程守护，父进程退出时子进程一定退出
        pro.daemon = True
        pro.start()


if __name__ == "__main__":
    main()
