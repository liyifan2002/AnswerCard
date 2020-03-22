import numpy as np
from imutils.perspective import four_point_transform
import imutils
import cv2

def recodot(img,wd,ht):#识别填涂点
    cnts = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    dots=[]
    for c in cnts:
          (x, y, w, h) = cv2.boundingRect(c)
          if wd*1.5>w>wd*0.5 and ht*1.6>h>ht*0.4:
                M = cv2.moments(c)
                dX = int(M["m10"] / M["m00"])
                dY = int(M["m01"] / M["m00"])
                cv2.circle(img, (dX, dY), 7, 128, -1)
                dots.append((dX, dY))
    return dots

def posdot(dots,wd,ht):#化为相对网格坐标
    pos=[]
    for d in dots:
        pos.append((d[0]//wd+1,d[1]//ht+1))
    return pos

def toanswer(pos,alist,default=""):
    answer={}
    for no,ans in alist.items():
        answer[no]=default
        for i in range(len(ans[1])):
            if((ans[0][0]+i,ans[0][1]) in pos):
                answer[no]+=ans[1][i]
    return answer