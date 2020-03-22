import sqlite3

conn = None
cur =None
def opendb(workd):
    global cur,conn
    conn = sqlite3.connect(workd+"/data.db",check_same_thread=False)
    cur = conn.cursor()


def stuinfo(group,no):#小组号确定
    global cur
    cursor = cur.execute('SELECT * FROM stulist WHERE "group"=%d AND "no"=%d'%(group,no))
    for r in cursor:
        return (r[0],r[3])
    return None

def stuname(stuid):#学生姓名确定
    global cur
    cursor = cur.execute('SELECT * FROM stulist WHERE "stuid"=%d'%stuid)
    for r in cursor:
        return (r[0],r[3])
    return None

def getResult(stuid):#获得试卷结果
    global cur
    result={"name":stuname(stuid)[1]}
    cursor = cur.execute('SELECT * FROM answerlist WHERE "stuid"=%d'%stuid)
    result["obj"]={}
    result["sub"]={}
    for r in cursor:
        if r[3]==1:# 客观题
            result["obj"][r[1]]=(r[2],r[4])
        else:#主观题
            result["sub"][r[1]]=(r[2],r[4])
    return result

def saveAns(stuid,quesn,ans,type_,score):
    global cur
    cur.execute("INSERT INTO answerlist VALUES (%s,'%s','%s','%s',%s)" % (stuid,quesn,ans,type_,score))#

def saveResult(result):#保存试卷结果
    global cur,conn
    stuid=result['stuid']
    cur.execute('DELETE FROM answerlist WHERE "stuid"=%d'%stuid)
    for n,a in result["obj"].items():
        saveAns(stuid,n,a[0],1,str(a[1]))
    for n,a in result["sub"].items():
        saveAns(stuid,n,a,2,"null")
    conn.commit()

def getSubAns(quesno):#互评
    global cur
    cursor = cur.execute('SELECT * FROM answerlist WHERE quesn="%s" AND score IS NULL LIMIT 0,1'%quesno)
    for c in cursor:
        return c
    return None

def markedscore(stuid,quesno,score):#互评
    global cur,conn
    cur.execute('UPDATE answerlist SET score=%s WHERE quesn="%s" AND stuid=%s and score IS NULL'%(score,quesno,stuid))
    conn.commit()

def getRank():
    global cur,conn
    cursor = cur.execute('SELECT s.name,s.stuid,sum(a.score) FROM answerlist a \
    JOIN stulist s on a.stuid = s.stuid GROUP BY a.stuid ORDER BY a.score DESC')
    return list(cursor)
    