def getCompanies():
    companies=[];
    f = open("F:\enterprise1.txt", encoding='utf-8')
    out = open("F:\enterprise22221.txt",mode='rw', encoding='utf-8')
    # 返回一个文件对象
    line = f.readline()  # 调用文件的 readline()方法
    while line:
        print(line),  # 后面跟 ',' 将忽略换行符
        # print(line, end = '')　　　# 在 Python 3中使用
        out.write(line)
        companies.append(line.replace("\n",""))
        line = f.readline()
    f.close()
    out.close()
    return companies

aaa=getCompanies()
print(aaa.size())