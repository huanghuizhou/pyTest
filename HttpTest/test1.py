import yzm

imgPath="/Users/hhz/test/yzm/yzm3.jpg"
res=yzm.getYzm(imgPath).replace(" ","")
print(str(res).strip())