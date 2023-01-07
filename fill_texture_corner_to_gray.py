#!/usr/bin/env python
# ecoding=utf-8

import os
import sys
import cv2 as cv
import numpy as np

filter = [".png", ".PNG"]  # 文件类型过滤


def all_path(dirname):
    result = []  # 所有的文件
    for maindir, subdir, file_name_list in os.walk(dirname):
        # print("1:",maindir) #当前主目录
        # print("2:",subdir) #当前主目录下的所有目录
        # print("3:",file_name_list)  #当前主目录下的所有文件
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)  # 合并成一个完整路径
            ext = os.path.splitext(apath)[1]  # 获取文件后缀 [0]获取的是除了文件名以外的内容
            if ext in filter:
                result.append(apath)
    return result


curPath = os.path.realpath(sys.argv[0])
curPath = curPath.replace(sys.argv[0], '')
allPath = all_path(curPath)

# for path in allPath:
#     print(path)

print('================================================Open CV', cv.__version__)

for path in allPath:
    img = cv.imread(path, cv.IMREAD_LOAD_GDAL)
    shape = img.shape
    width = shape[0]
    height = shape[1]
    allC = cv.split(img)
    # blueC, greenC, redC, alphaC =
    blueC = allC[0]
    greenC = allC[1]
    redC = allC[2]
    alphaC = 0
    # 判断是否存在透明通道，没有就创建
    if len(allC) >= 4:
        alphaC = allC[3]
    else:
        alphaC = np.ones((width, height), dtype=blueC.dtype) * 255

    # print(alphaC, isinstance(alphaC, list))

    # random.random()方法后面不能加数据类型
    img2 = np.ones((width, height), dtype=np.uint8)
    points_list = [
        (0, 0),
        (0, height - 1),
        (width - 1, height - 1),
        (width - 1, 0),
    ]
    for point in points_list:
        # cv.circle(img2, point, 3, (255, 156, 255), 1)
        img2[point[0], point[1]] = 255
    blueC = cv.addWeighted(img2, .1, blueC, 1, 0.0)
    greenC = cv.addWeighted(img2, .1, greenC, 1, 0.0)
    redC = cv.addWeighted(img2, .1, redC, 1, 0.0)
    alphaC = cv.addWeighted(img2, .1, alphaC, 1, 0.0)

    # img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
    # cv.cvtColor(img2, cv.COLOR_BGR2GRAY)

    # cv.imshow('blueC', blueC)
    # cv.imshow('greenC', greenC)
    # cv.imshow('redC', redC)
    # cv.imshow('alphaC', alphaC)

    result = cv.merge([blueC, greenC, redC, alphaC])
    cv.imwrite(path, result)
