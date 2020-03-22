import numpy as np
from imutils.perspective import four_point_transform
import imutils
import cv2
import obj_reco
import card
import template as te
from template import row, col, wd, ht


def autoresize(img):
    h, w = img.shape
    if w > h:
        if w > 1600:
            img = cv2.resize(img, (1600, int(h/w*1600)), cv2.INTER_LANCZOS4)
    else:
        if h > 1600:
            img = cv2.resize(img, (int(w/h*1600), 1600), cv2.INTER_LANCZOS4)
    return img


def fromimg(d, p_wd, p_rawimg):
    result = {}
    image = cv2.imread(p_wd+"/raw/"+p_rawimg)
    kernel = np.uint8(np.zeros((5, 5)))
    for x in range(5):
        kernel[x, 2] = 1
        kernel[2, x] = 1

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 灰度图
    gray = autoresize(gray)
    # cv2.imshow("raw", gray)
    paper = card.findcnt(gray)
    #cv2.imshow("area", paper)
    # cv2.waitKey()
    if paper.size < 10000:
        return -2
    paper = cv2.resize(paper, (row*wd, col*ht), cv2.INTER_LANCZOS4)
    paperth = cv2.adaptiveThreshold(
        paper, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 33, 7)
    paperth = cv2.morphologyEx(paper, cv2.MORPH_CLOSE, kernel)  # 二值化并进行开运算
    paperth = cv2.threshold(paper, 70, 255, cv2.THRESH_BINARY)[1]

    # 个人信息处理
    i_info = card.cut(paperth, te.a_info, wd, ht)
    d_info = obj_reco.recodot(i_info, wd, ht)
    #cv2.imshow("info_area", i_info)
    p_info = obj_reco.posdot(d_info, wd, ht)
    info = obj_reco.toanswer(p_info, te.a_info_list, 0)
    who = d.stuinfo(info["group"], info["no"])
    if who:
        result["stuid"] = who[0]
        result["name"] = who[1]

    else:
        return -1

    i_obj = card.cut(paperth, te.a_obj, wd, ht)
    d_obj = obj_reco.recodot(i_obj, wd, ht)
    #cv2.imshow("select_area", i_obj)
    p_obj = obj_reco.posdot(d_obj, wd, ht)
    ans_obj = obj_reco.toanswer(p_obj, te.a_obj_list)
    for n, a in ans_obj.items():  # 判分
        score = 0
        if te.ans_obj[int(n)-1] == a:
            score = te.a_obj_list[n][2]
        ans_obj[n] = (a, score)

    result["obj"] = ans_obj
    result["sub"] = {}
    for n, a in te.a_sub.items():
        i_ = card.cut(paper, a[0], wd, ht)
        #cv2.imshow("q%s_area" % n, i_)
        ans_t = "/%s/%d.jpg" % (n, result["stuid"])
        cv2.imwrite(p_wd+"/paper"+ans_t, i_)
        result["sub"][n] = ans_t
    d.saveResult(result)
    # cv2.waitKey()
    return result
