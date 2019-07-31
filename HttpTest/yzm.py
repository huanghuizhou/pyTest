import tesserocr

from PIL import Image, ImageDraw


#二值化
def binImg(img,binMax):
    img = img.convert('L')
    table = []
    for i in range(256):
        if i < binMax:
            table.append(0)
        else:
            table.append(1)

    img = img.point(table, '1')
    return img

# 二值数组
t2val = {}

#获取二值化数组
def twoValue(image, G):
    for y in range(0, image.size[1]):
        for x in range(0, image.size[0]):
            g = image.getpixel((x, y))
            if g > G:
                t2val[(x, y)] = 1
            else:
                t2val[(x, y)] = 0



# 根据一个点A的RGB值，与周围的8个点的RBG值比较，设定一个值N（0 <N <8），当A的RGB值与周围8个点的RGB相等数小于N时，此点为噪点
# G: Integer 图像二值化阀值
# N: Integer 降噪率 0 <N <8
# Z: Integer 降噪次数
# 输出
#  0：降噪成功
#  1：降噪失败
def clearNoise(image, N, Z):
    for i in range(0, Z):
        t2val[(0, 0)] = 1
        t2val[(image.size[0] - 1, image.size[1] - 1)] = 1

        for x in range(1, image.size[0] - 1):
            for y in range(1, image.size[1] - 1):
                nearDots = 0
                L = t2val[(x, y)]
                if L == t2val[(x - 1, y - 1)]:
                    nearDots += 1
                if L == t2val[(x - 1, y)]:
                    nearDots += 1
                if L == t2val[(x - 1, y + 1)]:
                    nearDots += 1
                if L == t2val[(x, y - 1)]:
                    nearDots += 1
                if L == t2val[(x, y + 1)]:
                    nearDots += 1
                if L == t2val[(x + 1, y - 1)]:
                    nearDots += 1
                if L == t2val[(x + 1, y)]:
                    nearDots += 1
                if L == t2val[(x + 1, y + 1)]:
                    nearDots += 1

                if nearDots < N:
                    t2val[(x, y)] = 1


def saveImage(filename, size):
    image = Image.new("1", size)
    draw = ImageDraw.Draw(image)

    for x in range(0, size[0]):
        for y in range(0, size[1]):
            draw.point((x, y), t2val[(x, y)])

    image.save(filename)


def getYzm(imgPath):

    #原图
    img=Image.open(imgPath)

    # #二值化阈值
    binMax=160
    # #二值化
    img=binImg(img,binMax)
    path = imgPath.replace('jpg', 'png')
    img.save(path)

    #二值化后图片
    binimg=Image.open(path)
    twoValue(binimg,binMax)
    #binimg.show()

    #降噪
    clearNoise(binimg,3,2)
    path1 = path.replace("png","jpeg")
    saveImage(path1, binimg.size)

    # 降噪后图片
    sbimg=Image.open(path1)

    res=tesserocr.image_to_text(sbimg)
    return res
