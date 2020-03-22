# 生成测验数据库
import csv
import sqlite3
import template

def genAnsTab(c):  # 生成答题表
    c.execute('''CREATE TABLE "answerlist" (
      "stuid" INTEGER NOT NULL,
      "quesn" TEXT,
      "answer" text,
      "type" integer,
      "score" real
    );''')
def genQuesTab(c, tmp):  # 生成题目表
    c.execute('''CREATE TABLE "questionlist" (
  "quesn" NOT NULL,
  "answer" text,
  "type" integer,
  "score" real,
  PRIMARY KEY ("quesn")
);''')

    for n, a in tmp.a_obj_list.items():## 添加客观题部分 type=1
        ans = tmp.ans_obj[int(n)-1]
        ascore = a[2]
        c.execute("INSERT INTO questionlist VALUES ('%s','%s',%d,%s)" % (n,ans,1,ascore))

    for n, a in tmp.a_sub.items():## 添加客观题部分 type=2
        ans = None
        ascore = a[1]
        c.execute("INSERT INTO questionlist VALUES ('%s','%s',%d,%s)" % (n,ans,2,ascore))

def genStuTab(c, f_stulist):  # 生成学生名单
    reader = csv.reader(f_stulist)
    c.execute('''CREATE TABLE "stulist" (
  "stuid" INTEGER NOT NULL,
  "group" INTEGER,
  "no" INTEGER,
  "name" TEXT(8),
  PRIMARY KEY ("stuid")
);''')
    n=0
    for row in reader:
        c.execute("INSERT INTO stulist VALUES (%s,%s,%s,'%s')" % tuple(row))
        n+=1
    return n
