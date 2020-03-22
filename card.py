import numpy as np
from imutils.perspective import four_point_transform
import imutils
import cv2


def findcnt(img):
    edged = cv2.Canny(img, 50, 150)  # 边缘图
    cnts = cv2.findContours(edged, cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)  # 寻找答题区边框
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    docCnt = None
    if len(cnts) > 0:
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)  # 按轮廓面积倒序
        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True) # 顶点数
            if len(approx) == 4:#四边形
                docCnt = approx
                break
    return four_point_transform(img, docCnt.reshape(4, 2) )# 四点变换并裁切


def cut(img, area, wd, ht): # 裁切相应区域
    return img[(area[1]-1)*ht:area[3]*ht, (area[0]-1)*wd:area[2]*wd]

def areasize(ax,ay,bx,by):
    return (bx-ax,by-ay)