import logging
import time

import pymysql

DB_HOST = '192.168.2.203'
DB_USER = 'greatTao'
DB_PASSWD = 'greatTao.1314'
DB_PORT = 3306

# DB_HOST = 'localhost'
# DB_USER = 'root'
# DB_PASSWD = '123456'
# DB_PORT = 3306
gttown_crm_db = pymysql.connect(host=DB_HOST,  # 192.168.100.254
                                          user=DB_USER,
                                          passwd=DB_PASSWD,
                                          db="gttown_crm",
                                          port=DB_PORT,  # 3306
                                          use_unicode=True,
                                          charset="utf8")


def get_logger(name):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    # Standard output handler
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(logging.Formatter('%(levelname)s - %(name)s:%(lineno)s: %(message)s'))
    log.addHandler(sh)
    return log


logger = get_logger(__file__)

def doDelCF():
    with gttown_crm_db.cursor() as cursor:
        cursor.execute(
            "select id from channel_customer where requirement_remark = 'CF' ")
        ids = cursor.fetchall()
    count=0
    for id in ids:
        sql1 = """delete from channel_contact where customer_id=%s"""
        sql2 = """delete from channel_product where customer_id=%s"""
        sql3="""delete from channel_customer where id=%s"""
        try:
            with gttown_crm_db.cursor() as cursor:
                cursor.execute(sql1,id)
                cursor.execute(sql2,id)
                cursor.execute(sql3,id)
                count+=1
                if(count%500==0):
                    gttown_crm_db.commit()
                    print("_________________________________________")
                print(id, 'del success')
        except Exception as e:
            gttown_crm_db.commit()
            logger.warning('Failed to del id %s' % id, e)
            time.sleep(2)







def main():
    doDelCF()
    logger.info("del success")



if __name__ == '__main__':
    main()
