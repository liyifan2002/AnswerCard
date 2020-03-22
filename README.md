# AnswerCard

## 答题卡识别+网上阅卷 基于Python+OpenCV+flask+sqlite


本人河南2020高三党一枚 由于疫情宅家学习 平时组织考试同学互改效率很低

于是想起了去年写的这个程序 其中图像识别部分程序在初中毕业前就已基本完成

当时为了参加程序设计比赛周末只花了一天时间整理了下 功能非常简陋

而且没有系统学过程序设计 各模块较混乱

现在迫于学业压力也没有精力再进行完善

**希望能分享给各路大神借鉴/开发**

## 思路及原理
用excel表格 按比例制作答题卡，并将外框加粗。

手机拍照后通过flask web上传，后端openCV识别答题区域边框并裁切

客观题自动识别填涂点位置 主观题按比例位置裁切

教师/学生通过web阅卷判分 最后汇总得分

## 使用说明
```pip install imutils==0.4.3 numpy==1.13.3 opencv-python==3.3.0.10 scipy==1.0.0 flask==1.0.2 -i https://pypi.tuna.tsinghua.edu.cn/simple some-package```

先编辑好member.csv 学生名单，答题卡模板.xslx，并将对应的题目信息修改template.py

再执行python main.py 按提示生成数据库文件 并启动web服务器

Web服务器默认端口5000
```
├─source
│  │  card.py #答题卡检测模块
│  │  main.py #生成数据库模块
│  │  obj_reco.py #填涂识别模块
│  │  proce.py #图像处理模块
│  │  runserver.py #web服务器启动
│  │  template.py #答题卡配置文件
│  │
│  ├─data #数据存放目录
│  ├─db #数据库相关模块目录
│  │    DB.py #数据库操作模块
│  │    gendb.py #数据库创建模块
│  └─templates #网页模板文件
│          correct.html #批改页模板
│          rank.html #排名页模板
│          result.html #个人答案页模板
│          success.html #上传成功模板
│          upload.html #上传页模板
URL
/ 上传图片
/result/<id> 批改结果
/correct/<id> 批改指定题目
/rank 得分排名
```

## 中国加油！
