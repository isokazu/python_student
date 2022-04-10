import pymysql

data = pymysql.connect(host="81.70.133.161",
                       user="root",
                       password="csy123,",
                       port=3306,
                       database="dict")

cur = data.cursor()

insert_sql = "INSERT INTO dict_table (word, idea) VALUES (%s, %s)"

file_dir = "./dict.txt"
with open(file_dir, "r", encoding="utf8") as f:
    for line in f:
        table = line.split(" ")
        head = table[0]
        body = " ".join(table[1:]).strip()
        try:
            cur.execute(insert_sql, [head, body])
            data.commit()
        except Exception as e:
            data.rollback()
            print(e)


cur.close()
data.close()
print("success")
