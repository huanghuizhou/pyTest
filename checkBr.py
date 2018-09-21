import bcrypt
import sys
print(sys.argv[1].encode())
print(sys.argv[2].encode())

print(bcrypt.checkpw(sys.argv[1].encode(),sys.argv[2].encode()))
#print(bcrypt.hashpw(sys.argv[1].encode(), bcrypt.gensalt(prefix=b'2a')).decode())