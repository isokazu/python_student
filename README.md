# 电子辞典

### 技术方案：

1. socket TCP通信搭建
2. pymysql 数据库操作
3. Process 子进程处理IO（子进程无法使用标准输入）
4. getpass 终端输入隐藏显示（用法与input相同）
5. hashlib 明文密码转换加密，哈希加密算法（加盐法）
6. signal 信号，用于处理僵尸进程（win不可用）

### 数据表结构：

**表1：用户表**（用来存储注册用户信息）

* id；主键，方便查询
* name：用户名
* passwd：登录密码
* create_time：注册时间

```sql
CREATE TABLE user_table 
(id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
name VARCHAR(32) NOT NULL,
passwd VARCHAR(128) NOT NULL,
create_time DATETIME DEFAULT now() NOT NULL);
```

---
**表2：历史记录**（方便用户查询历史记录）

* id：便于索引查找
* name：用户姓名
* word：历史查询单词
* time：历史查询时间

```sql
CREATE TABLE history_table 
(id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
name VARCHAR(32) NOT NULL,
word VARCHAR(28) NOT NULL,
create_time DATETIME DEFAULT now() NOT NULL);
```

### 开发结构：

* C/S模型
* server：
    * 数据库处理模块
    * tcp套接字通信模块
* client：
    * main

### 功能分析和通信搭建：

* 用户注册协议：
    * "REGISTER_AGREEMENT\nUSER: 用户名\nPASSWD: 密码"
    * 服务端：成功返回"register_success"
* 用户登录协议：
    * "SIGN_IN_AGREEMENT\nUSER: 用户名\nPASSWD: 密码"
    * 服务端：成功返回"sign_in_success"
* 用户退出协议：
    * "\*DICT_USER_EXIT*\n"
* 查询单词协议：
    * "CLIENT_WORD\n用户ID\n单词"
* 查询历史记录协议：
    * "CLIENT_HISTORY\n用户姓名"

### 功能逻辑介绍：

**client**

一级页面

1. 注册：
    * user填写用户名
    * passwd填写密码
    * 回车后提交到服务端数据库
2. 登录：
    * 填写用户名与密码，提交到数据库进行数据比对
3. 退出：
    * 退出客户端

二级页面

1. 查单词：
    * 输入要查询的单词
2. 历史记录：
    * 查看最近10条查询的历史记录
3. 注销：
    * 退出二级登录页面，返回到一级页面

**server**

* 数据库查询模块
    * user_in_database(user)：查询用户是否存在，存在返回用户的ID和密码，不存在返回False
    * insert_user(user, passwd)：插入用户名和密码，成功返回"insert ok"，失败返回False
    * select_word(word)：查询单词，成功返回元组类型的(单词, 解释)，失败返回False
    * insert_history(user_id, word)：插入当前正在查询单词的用户的ID和单词
    * select_history(user_id)：根据用户ID查询当前用户的历史记录(前10条)

