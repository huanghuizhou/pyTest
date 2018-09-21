
# coding=utf-8
import bcrypt
import sys
print("salt",bcrypt.gensalt(prefix=b'2a'))
print(bcrypt.hashpw(sys.argv[1].encode(), bcrypt.gensalt(prefix=b'2a')).decode())
# b=bcrypt.hashpw(sys.argv[1].encode(), bcrypt.gensalt(prefix=b'2a')).decode()
# print(b)
# a=input("输入")
# print(a)
# print(b)
# c=bcrypt.checkpw(sys.argv[1].encode(),b)
# print(c)