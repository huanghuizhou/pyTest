import requests
print ("downloading with requests")
url = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1527593234524&di=c54729ff719b2435245b39de87ab9238&imgtype=0&src=http%3A%2F%2Fi3.cnfolimg.com%2Ffile%2F201804%2F1_201804271547203702.jpg'
r = requests.get(url)
with open("G:/", "wb") as code:
     code.write(r.content)