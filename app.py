from flask import Flask,render_template,request,redirect, url_for
import os
import io
import csv

import pandas as  pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import numpy as np
import joblib


app=Flask(__name__)

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/login_chuli",methods=['POST'])
def login_chuli():
    username=request.form.get("username")
    password=request.form.get("password")
    if username == "d" and password == "d":  #登录验证，不连接数据库写死
        return render_template("index.html")
    else:
        return render_template("login.html",msg="密码错误")

        
@app.route("/uploadfile",methods=['POST'])
def upload():
    global f #声明全局变量，其它路由内可以调用
    f = request.files['file1']  #接收上传的文件
    basepath=os.path.dirname(__file__)
    upload_path = os.path.join(basepath, 'uploads',"da.csv") #设置文件路径和文件名
    f.save(upload_path) #保存文件
    return redirect(url_for('ml')) #重定向到路由/ml

@app.route("/ml")
def ml():
    global data
    data=pd.read_csv(r'./uploads/da.csv',index_col = 0)
    #保存data.info()的内容
    buf = io.StringIO()
    data.info(buf=buf)
    info = buf.getvalue()
    with open('./uploads/data_info.txt','r+',encoding='utf-8') as f:
        f.truncate()
        f.write(info)
        f.flush()
    return  render_template("main.html")
    
@app.route("/cleandata",methods=['POST'])
def cleandata():
    value=request.form.get("yes")
    if value == "yes":
        labels = list(data.columns.values)
        return str(labels)
    else:
        return "no"



if __name__ == "__main__":
    app.run(host='0.0.0.0',port=80, debug=False,threaded=True) #启动一个flask项目