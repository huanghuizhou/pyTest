import json

out=open('aaa.json',"w")
dataDict = {'company': 123123121, 'country': "1231231231", 'product': str(123123123)}



json_str = json.dumps(dataDict, ensure_ascii=False, indent=2)
out.write(json_str)
out.flush()
out.close()
print(1)
def aaa():
    global aa
    aa="asd"


def bbb():
    print(aa)



aaa()
bbb()
print(aa)