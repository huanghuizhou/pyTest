sql_save2 = """INSERT INTO luyunfeixiang\
                                  (businessno, box1, boxcount1, box2, boxcount2, box3, boxcount3, box4, boxcount4, fleet,fleetlinkman,fleetmobile,getcy,uptime) value\
                                  (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

print('Failed to insert into luyunfeixiang sql is %s' % sql_save2)

a=""
if a:
    print(a)
else:
    print(123)



for i in range(10):
    if i==7:
        print(123)
        continue
    print(i)

print("ok")