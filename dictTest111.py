aa={"aaaa":123,"bbb":222,'ccc':12,'ddd':55}

print(lambda aa:aa[1])
dict111= sorted(aa.items(), key=lambda d:d[1], reverse = True)

print(str(dict111))

aaa=dict(dict111)
print(aaa)
print(11)

