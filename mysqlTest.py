import pymysql


DB_HOST = '192.168.2.203'
DB_USER = 'greatTao'
DB_PASSWD = 'greatTao.1314'
DB_PORT = 3306

# DB_HOST = '192.168.2.203'
# DB_USER = 'greattao'
# DB_PASSWD = 'greatTao.5877'
# DB_PORT = 3308
OUT_FILE = './result.csv'

# 打开mysql数据库链接


gttown_crm_db = pymysql.connect(host=DB_HOST,  # 192.168.100.254
                                user=DB_USER,
                                passwd=DB_PASSWD,
                                db="gttown_crm",
                                port=DB_PORT,  # 3306
                                use_unicode=True,
                                charset="utf8",
                                cursorclass=pymysql.cursors.DictCursor)

cursor = gttown_crm_db.cursor()
sql = """select * from channel_customer"""
cursor.execute(sql)
results = cursor.fetchall()
print(results)


