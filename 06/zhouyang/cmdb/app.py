#coding:utf-8

from flask import Flask
from flask import render_template  #跳转到一个路由，执行路由下的整个def逻辑。与下面的redirect有区别！
from flask import request
from flask import redirect  #跳转到一个页面，不执行def逻辑
from flask import session
from functools import wraps  #解决多层装饰器中，上层会错误的获取到下层装饰器的__name__的bug
from flask import flash  #消息闪现

import sys
reload(sys)
sys.setdefaultencoding('utf8')


app=Flask(__name__)
app.secret_key='jidjai2jixjaix0xjajxj292jd'  #session加密

def checkinfo(func):
    '''装饰器，验证用户信息'''
    @wraps(func)
    def wrapper(*args,**kwargs):
        if not session.get('user'):
            return redirect('/')
        rt=func()
        return rt
    return wrapper

@app.route('/')
def index():
    #return redirect('/login/')  不能这样转，这样会执行/login/的验证逻辑，所以会导致首页跳过去之后提示用户名错误信息。
    return render_template('login.html')

@app.route('/logs/')
@checkinfo
def log_topn():
    cnt=request.args.get('topn',10)
    cnt= int(cnt) if str(cnt).isdigit() else 10

    import get_topn
    rt_list=get_topn.get_topn(cnt)
    return render_template('topn.html',n=cnt,rt_list=rt_list)

@app.route('/login/',methods=['GET','POST']) #不注明methods则默认是GET方法
def login():
    params=request.args if request.method == 'GET' else request.form
    username=params.get('username','')
    password=params.get('password','')
    #import login
    import userdb as login
    if login.check_user(username,password):
        session['user']={'username':username}  #用户信息验证通过后，将信息存储到session中
        flash('登陆成功')
        return redirect('/logs/')
    else:
        return render_template('login.html',username=username,error='您输入的用户名或密码错误!')

@app.route('/userinfo/')
@checkinfo
def userinfo():
    print session
    #import login
    import userdb as login
    import uconf
    #user_list=login.get_users(uconf.user_conf)
    user_list=login.get_users()
    return render_template('show_users.html',user_list=user_list)

@app.route('/readytoadduser/',methods=['POST'])
def readytoadduser():
    return render_template('readytoadduser.html')

@app.route('/user/create/',methods=['GET','POST'])
def adduser():
    import adduser
    params=request.args if request.method == 'GET' else request.form
    username=params.get('username','')
    password=params.get('password','')
    age=params.get('age','')
    age=int(age) if str(age).isdigit() else ''
    if username and password and age:
        if adduser.adduser(username,password,age):
            flash('用户注册成功')  #消息闪现方式
            return render_template('adduser.html',res='用户名注册成功')  #传参渲染方式
        else:
            return render_template('adduser.html',fres='用户名已存在，请重新注册')
    else:
        flash('请写全注册信息')
        return render_template('adduser.html',fres='注册信息不全，请重新注册',user=username)


@app.route('/readytousermodify/',methods=['GET','POST'])
@checkinfo
def readytousermodify():
    username=request.args.get('username','')
    return render_template('readytousermodify.html',username=username)

@app.route('/usermodify/',methods=['GET','POST'])
@checkinfo
def usermodify():
    import usermodify
    params=request.args if request.method == 'GET' else request.form
    username=params.get('username','')
    password=params.get('password','')
    age=params.get('age','')
    age=int(age) if str(age).isdigit() else ''
    print usermodify.usermodify(username,password,age)
    if usermodify.usermodify(username,password,age):
        return render_template('modify_ok.html',username=username,ok_r="用户修改成功")
    else:
        return render_template('modify_ok.html',username=username,error_r="用户修改失败")
    #return redirect('/usermodify/?username=')

@app.route('/logout/')
def logout():
    session.clear()
    return render_template('login.html')

if __name__=='__main__':
    app.run(host='192.168.0.102',port=8080,debug=True)
