import pymysql


class DoDatabase:
    def __init__(self, host="127.0.0.1", user="root", password="csy123,", database="dict", port=3306,
                 charset="utf8"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.charset = charset
        self.sql_select_word = "SELECT word, idea FROM dict_table WHERE word=%s;"
        self.sql_select_user = "SELECT passwd FROM user_table WHERE name=%s;"
        self.sql_select_history = "SELECT word FROM history_table WHERE name=%s ORDER BY create_time DESC LIMIT 10;"

        self.sql_insert_user = "INSERT INTO user_table (name, passwd) VALUES (%s,%s);"
        self.sql_insert_history = "INSERT INTO history_table (name, word) VALUES (%s,%s);"

        self.sql_delete_user = "DELETE TABLE user_table WHERE name=%s"

        self.__create_database()

    # 创建数据库
    def __create_database(self):
        self.data = pymysql.connect(host=self.host,
                                    user=self.user,
                                    password=self.password,
                                    database=self.database,
                                    port=self.port,
                                    charset=self.charset)

    # 创建游标
    def create_cul(self):
        cul = self.data.cursor()
        return cul

    # 关闭游标
    def delete_cul(self, cul):
        cul.close()

    # 关闭数据库
    def delete_database(self):
        self.data.close()

    # 查看用户是否存在
    def user_in_database(self, user, cul):
        cul.execute(self.sql_select_user, [user])
        result = cul.fetchall()
        if not result:
            return False
        else:
            return result[0]

    # 插入用户
    def insert_user(self, user, passwd, cul):
        try:
            cul.execute(self.sql_insert_user, [user, passwd])
            self.data.commit()
        except Exception:
            self.data.rollback()
            return False
        return "insert ok"

    # 查询单词
    def select_word(self, word, cul):
        cul.execute(self.sql_select_word, [word])
        result_idea = cul.fetchall()
        if not result_idea:
            return False
        else:
            return result_idea[0]

    # 存储历史记录
    def insert_history(self, user_id, word, cul):
        try:
            cul.execute(self.sql_insert_history, [user_id, word])
            self.data.commit()
        except Exception as e:
            self.data.rollback()
            return False
        return "ok"

    # 查看历史记录
    def select_history(self, user_id, cul):
        cul.execute(self.sql_select_history, [user_id])
        word = cul.fetchall()
        if not word:
            return False
        else:
            word_list = []
            for item in word:
                word_list.append(item[0])
            return word_list


if __name__ == "__main__":
    db = DoDatabase()
    cul = db.create_cul()
    result = db.user_in_database("管理员", cul)
    word = db.select_history(2, cul)
    print(result)
