from flask import Flask
from flask import render_template
from flask import request, Response
import time
import os
import sys
import db.DB

app = Flask(__name__)
workdir = ""


@app.route('/')
def index():
    return render_template('upload.html')


@app.route('/cardimg', methods=['POST'])
def upload():
    timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    if request.method == 'POST':
        f = request.files['card']
        f.save(workdir + "/raw/"+timestamp+".jpg")
        import proce
        r = proce.fromimg(db.DB, workdir, timestamp+".jpg")
        if r == -2:
            return "图像识别错误，请尝试重新拍摄"
        if r == -1:
            return "未找到学生信息"
        db.DB.saveResult(r)
        return render_template("success.html", r=r)


@app.route('/cardimg/<qno>/<who>')
def showimg(who, qno):
    with open("%s/paper/%s/%s" % (workdir, qno, who), 'rb') as image:
        image = image.read()
        resp = Response(image, mimetype="image/jpeg")
        return resp


@app.route('/result/<stuid>')
def showres(stuid):
    r = db.DB.getResult(int(stuid))
    return render_template("result.html", r=r)


@app.route('/correct/<qno>')
def correct(qno):
    t = db.DB.getSubAns(qno)
    if t == None:
        return "啊哈，没有可以批改的了"
    return render_template("correct.html", quesno=qno, stuid=t[0], a=t[2])


@app.route('/correct', methods=['POST'])
def marked():
    if request.method == 'POST':
        quesno = request.form['quesno']
        stuid = request.form['stuid']
        score = request.form['score']
        db.DB.markedscore(stuid, quesno, score)
        return '成功，<a href="/correct/%s">再改一份</a>' % quesno


@app.route('/rank')
def rank():
    ranks = db.DB.getRank()
    return render_template("rank.html", ranks=ranks)


if __name__ == '__main__' and len(sys.argv) > 1:
    workdir = sys.argv[1]
    db.DB.opendb(os.path.abspath(workdir))
    print("正在启动web服务器")
    app.run('0.0.0.0')
