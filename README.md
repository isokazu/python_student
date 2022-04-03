# 随机图片
* 从本地数据库读取图片上传到http
---
### 技术点
1. 套接字的使用
2. pymysql连接数据库
3. py线程的使用
4. http协议处理
---
### 数据库格式
```sql
CREATE TABLE image_db 
(id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
image LONGBLOB DEFAULT NULL);
```
