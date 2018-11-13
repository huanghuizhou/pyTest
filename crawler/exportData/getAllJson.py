import json
import logging
import os


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




out = open('./allJson.json', 'w')


numAll=0

def doMerge(jsonPath):
    dataOpen = open(jsonPath)
    dataList = json.loads(dataOpen.read())

    for dictDate in dataList:
        if(len(dictDate)==0):
            continue

        dictDate['company']=str(dictDate['company']).replace('\"','').replace('\'','')

        if "industry" in dictDate:
            dictDate['industry']=int(dictDate['industry'])

        json_str = json.dumps(dict(dictDate), ensure_ascii=False, indent=2)
        out.write(json_str+',')


    global numAll
    numAll += len(dataList)


    print(jsonPath+' merge success')

def main():
    fileinName = './json'
    out.write('[')


    list = os.listdir(fileinName)
    #历届广交会名单
    for i in range(0, len(list)):
        path = os.path.join(fileinName, list[i])
        #xxx届广交会
        if(path=='./json/.DS_Store'):
            continue
        filelist = os.listdir(path)
        #11x届广交会
        for j in range(0, len(filelist)):
            filePath = os.path.join(path, filelist[j])
            if os.path.isdir(filePath):
                jsonlist = os.listdir(filePath)
                jsonlist.reverse()
                #json
                for k in range(0, len(jsonlist)):
                    jsonPath = os.path.join(filePath, jsonlist[k])
                    doMerge(jsonPath)

                print("——————————————————————————————————")



    #out.write(str(listAll))
    out.write('{}')
    out.write(']')

    out.flush()
    out.close()
    print(numAll)

if __name__ == '__main__':
    main()
