import hashlib
import time

md = hashlib.md5()#构造一个md5


salt="11111111111111111111111111000000"

def md5_passwdis(str):
    #satl是盐值
    str=salt+str
    md.update(str.encode())
    res = md.hexdigest()
    return res


date=time.time()

print(md5_passwdis(str(date)))


print(str(bin(4294967232)))