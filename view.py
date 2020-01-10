from flask import Flask, render_template, redirect, url_for, request, flash, session
import db.query
import wtf
import pymysql
import time
import recommend_algorithm

todayDate = time.strftime("%Y-%m-%d", time.localtime())
view = Flask(__name__)
view.secret_key = 'wprofessor'


# @view.route('/main/')
# def hello_world():
#     return render_template('index.html')


@view.route('/Test/', methods=['GET', 'POST'])
def testDemo():
    return render_template('test.html')


# 我的预订
@view.route('/my_reservation/', methods=['GET', 'POST'])
def myReservation():
    conn = pymysql.connect(host="127.0.0.1", user="wprofessor", password="Aa*123456", database="DBMeeting",
                           charset="utf8")
    cursor = conn.cursor()
    sql = 'select 用户id from 用户 where 账号=' + session.get('account') + ';'
    try:
        cursor.execute(sql)
        ID = cursor.fetchall()[0][0]
        result = db.query.myReservation(ID)
        if session.get('account') == '111111':
            return render_template('my_reservation.html', result=result, name=session.get('name'))
        else:
            return render_template('my_reservation_user.html', result=result, name=session.get('name'))
    except:
        flash('数据库异常')
        return render_template('my_reservation.html', result=(()), name=session.get('name'))


# 删除预订
# @view.route('/my_reservation/', methods=['GET', 'POST'])

# 我的会议
@view.route('/my_meeting/', methods=['GET', 'POST'])
def myMeeting():
    conn = pymysql.connect(host="127.0.0.1", user="wprofessor", password="Aa*123456", database="DBMeeting",
                           charset="utf8")
    cursor = conn.cursor()
    sql = 'select 用户id from 用户 where 账号=' + session.get('account') + ';'
    result = ()
    try:
        cursor.execute(sql)
        ID = cursor.fetchall()[0][0]

        result = db.query.myMeeting(ID)
        print(result, ID, session.get('account'))
    except:
        flash('数据库异常')
    if session.get('account') == '111111':
        return render_template('my_meeting.html', result=result, name=session.get('name'))
    else:
        return render_template('my_meeting_user.html', result=result, name=session.get('name'))


# 修改用户信息
@view.route('/change_user/', methods=['GET', 'POST'])
def changeUserInformation():
    sexDict = {0: '男', 1: '女'}
    departmenntDict = {'one': '人力资源部', 'two': '企划部', 'three': '市场部', 'four': '财务部'}

    userForm = wtf.userInformation()
    if request.method == 'POST':
        account = request.form.get('account')
        password = request.form.get('password')
        password1 = request.form.get('password1')
        contact = request.form.get('contact')
        sex = request.form.get('sex')
        departmentSelect = request.form.get('departmentSelect')
        # print(account, contact, sex, departmentSelect)
        conn = pymysql.connect(host="127.0.0.1", user="wprofessor", password="Aa*123456", database="DBMeeting",
                               charset="utf8")
        cursor = conn.cursor()
        sql = 'select 密码 from 用户 where 账号=' + str(account)
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            if results:
                if results[0][0] == password:
                    # print(password1, contact, sexDict[sex], departmenntDict[departmentSelect])
                    if len(password1) >= 6:
                        # print(password1,contact, sexDict[sex],departmenntDict[departmentSelect])

                        sqlList = ['update 用户 set 密码=' + password1 + ' where 账号=' + str(account),
                                   'update 用户 set 联系方式=' + contact + ' where 账号=' + str(account),
                                   'update 用户 set 性别=\'' + sexDict[int(sex)] + '\' where 账号=' + str(account),
                                   'update 用户 set 部门=\'' + str(
                                       departmenntDict[departmentSelect]) + '\'  where 账号=' + str(account)]
                        try:
                            for i in sqlList:
                                print(i)
                                cursor.execute(i)
                                conn.commit()
                            flash('修改成功')
                        except:
                            flash('更新有误')
                            print('更新失败')
                            conn.rollback()
                    else:
                        flash('新密码有误')
                else:
                    flash('旧密码有误')
            else:
                flash('账号不存在')

        except:
            print("查询用户表失败")
            flash('查询用户表失败')
        cursor.close()
        conn.close()
    return render_template('change_user_information.html', userForm=userForm, name=session.get('name'))


# 注册审批
@view.route('/register_check/', methods=['GET', 'POST'])
def registerAndCheck():
    results = db.query.lookAllRegister()
    results_user = []
    for row in results:
        tump = list(row)
        tump.append('同意')
        results_user.append(tump)
    return render_template('register_check.html', results_user=results_user, name=session.get('name'))


# 添加用户
@view.route('/register_check/<user_ID>/', methods=['GET', 'POST'])
def addUser(user_ID):
    print(user_ID)
    conn = pymysql.connect(host="127.0.0.1", user="wprofessor", password="Aa*123456", database="DBMeeting",
                           charset="utf8")
    cursor = conn.cursor()

    sql1 = 'select id,name,账号,密码,联系方式,sex,部门 from 审批表 where id=' + user_ID + ';'
    try:
        cursor.execute(sql1)
        result = cursor.fetchall()
        print(result)
    except:
        print('查询审批表失败')
    sql1 = 'insert into 用户(用户id,姓名,账号,密码,联系方式,性别,部门) values (%s,%s,%s,%s,%s,%s,%s);'
    sql2 = 'delete from 审批表 where id = ' + user_ID + ';'
    try:
        cursor.execute(sql1, [result[0][0], result[0][1], result[0][2], result[0][3], result[0][4], result[0][5],
                              result[0][6]])
        cursor.execute(sql2)
        conn.commit()
        flash('添加成功')
    except:
        conn.rollback()
        flash('添加失败')
    cursor.close()
    conn.close()
    return redirect(url_for('registerAndCheck'))


# 查询用户
@view.route('/search_user/', methods=['GET', 'POST'])
def searchUser():
    results = db.query.selectUser()
    results_user = []
    for row in results:
        tump = list(row)
        tump.append('删除')
        results_user.append(tump)
    return render_template('search_user.html', results_user=results_user, name=session.get('name'))


# 删除用户
@view.route('/search_user/<searchUserID>/', methods=['GET', 'POST'])
def deleteUser(searchUserID):
    print(searchUserID)
    conn = pymysql.connect(host="127.0.0.1", user="wprofessor", password="Aa*123456", database="DBMeeting",
                           charset="utf8")
    cursor = conn.cursor()
    sql1 = 'select * from 会议 where 预订者id = ' + searchUserID + ';'
    sql2 = 'select * from 选会议表 where 用户id = ' + searchUserID + ';'
    try:
        cursor.execute(sql1)
        result1 = cursor.fetchall()
        cursor.execute(sql2)
        result2 = cursor.fetchall()
        if result1 or result2:
            flash('删除失败，该用户有正在执行的业务')
        else:
            sql = 'delete from 用户 where 用户id = ' + searchUserID + ';'
            try:
                cursor.execute(sql)
                conn.commit()
                flash('删除成功')
            except:
                conn.rollback()
    except:
        flash('数据库异常，删除失败')
    cursor.close()
    conn.close()
    return redirect(url_for('searchUser'))


# 查看会议室
@view.route('/look_meetingroom/', methods=['GET', 'POST'])
def lookMeetingRoom():
    results = db.query.lookMeetingRoom()
    results_user = []
    for row in results:
        tump = list(row)
        tump.append('修改')
        tump.append('删除')
        results_user.append(tump)
    if session.get('account') == '111111':
        return render_template('look_meetingroom.html', results_user=results_user, name=session.get('name'))
    else:
        return render_template('look_meetingroom_user.html', results_user=results_user, name=session.get('name'))


# 删除会议室
@view.route('/look_meetingroom/<meetingRoomID>/', methods=['GET', 'POST'])
def deleteMeetingRoom(meetingRoomID):
    print(meetingRoomID)
    conn = pymysql.connect(host="127.0.0.1", user="wprofessor", password="Aa*123456", database="DBMeeting",
                           charset="utf8")
    cursor = conn.cursor()
    sql1 = 'select * from 会议 where 会议室id=' + meetingRoomID + ';'
    try:
        cursor.execute(sql1)
        result = cursor.fetchall()
        if result:
            flash('此会议室被预定，删除失败')
        else:
            sql1 = 'delete from 会议室 where 会议室id=' + meetingRoomID + ';'
            try:
                cursor.execute(sql1)
                conn.commit()
                flash('删除成功')
            except:
                conn.rollback()
                flash('删除异常')
    except:
        flash('数据库异常，删除失败')
    cursor.close()
    conn.close()
    return redirect(url_for('lookMeetingRoom'))


# 修改会议室
@view.route('/update_meetingroom/<mrid>/', methods=['GET', 'POST'])
def updateMeetingRoom(mrid):
    print(mrid)
    form = wtf.updataMR()
    conn = pymysql.connect(host="127.0.0.1", user="wprofessor", password="Aa*123456", database="DBMeeting",
                           charset="utf8")
    cursor = conn.cursor()
    sql = 'select * from 会议室 where 会议室id=' + mrid + ';'
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
    except:
        print('初始化默认值失败')
    id = request.form.get('mrID')
    mrName = request.form.get('mrName')
    mrCapacity = request.form.get('mrCapacity')
    mrContent = request.form.get('mrContent')
    if request.method == 'POST':
        sql = 'select * from 会议 where 会议室id=' + mrid + ';'
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            if result:
                flash('此会议室已被预订，不能修改')
            else:
                sqlList = ['update 会议室 set 会议室id=' + id + ' where 会议室id=' + mrid + ';',
                           'update 会议室 set 会议室名字=\'' + mrName + '\' where 会议室id=' + mrid + ';',
                           'update 会议室 set 会议室容量=' + mrCapacity + ' where 会议室id=' + mrid + ';',
                           'update 会议室 set 说明=\'' + mrContent + '\' where 会议室id=' + mrid + ';']

                for i in sqlList:
                    try:
                        cursor.execute(i)
                        conn.commit()
                    except:
                        conn.rollback()
                        flash('修改失败')
                flash('修改成功')
        except:
            flash('数据库异常，修改失败')

    cursor.close()
    conn.close()
    return render_template('update_meetingroom.html', form=form, results=results, name=session.get('name'))


# 查看会议
@view.route('/look_meeting/', methods=['GET', 'POST'])
def lookMeeting():
    results = db.query.loolMeeting()
    results_user = []
    for row in results:
        tump = list(row)
        tump.append('参与')
        tump.append('删除')
        results_user.append(tump)

    conn = pymysql.connect(host="127.0.0.1", user="wprofessor", password="Aa*123456", database="DBMeeting",
                           charset="utf8")
    cursor = conn.cursor()

    for row in results_user:
        print(row)
        if row[6] < todayDate:
            sql = 'delete from 会议  where 会议id=%s' + ';'
            sql1 = 'delete from 选会议表 where 会议id=%s' + ';'

            try:
                cursor.execute(sql1, row[0])
                conn.commit()
                flash('删除成功')
            except:
                flash('数据库异常')
                conn.rollback()
            try:
                cursor.execute(sql, row[0])
                conn.commit()

            except:
                flash('数据库异常')
                conn.rollback()

    cursor.close()
    conn.close()

    if session.get('account') == '111111':
        return render_template('look_meeting.html', results_user=results_user, name=session.get('name'))
    else:
        return render_template('look_meeting_user.html', results_user=results_user, name=session.get('name'))


# join会议
@view.route('/look_meeting/<mID>/<userID>/', methods=['GET', 'POST'])
def joinMeeting(mID, userID):
    print(mID, userID)
    conn = pymysql.connect(host="127.0.0.1", user="wprofessor", password="Aa*123456", database="DBMeeting",
                           charset="utf8")
    cursor = conn.cursor()
    sql = 'select * from 会议 where 会议id = ' + mID + ' and 预订者id = ' + userID + ';'
    try:
        sql1 = 'select 用户id from 用户 where 账号 =  ' + session.get('account') + ';'
        cursor.execute(sql1)
        userid = cursor.fetchall()[0][0]
        cursor.execute(sql)
        results = cursor.fetchall()
        print(results)
        sql1 = 'select 会议室容量 from 会议室 where 会议室id = %s' + ';'
        sql2 = 'select * from 选会议表 where 用户id = %s and 会议id = %s' + ';'
        cursor.execute(sql1, results[0][3])
        result_c_m = cursor.fetchall()
        cursor.execute(sql2,[userid,mID])
        result_exist = cursor.fetchall()
        print('===========================================================')
        print(result_exist)
        capacity = result_c_m[0][0]

        print(capacity)
        if results[0][4] >= capacity:
            flash('会议人数已满，拒绝参与')
        elif result_exist:
            flash('会议已参加，请勿重返参加，给别人也留点机会，做人留一线，日后好想见！！！')
        else:

            sql1 = 'insert into 选会议表(用户id,会议室id,会议id,会议名) values(%s,%s,%s,%s);'
            try:
                cursor.execute(sql1, [userid, results[0][3], mID, results[0][1]])
                conn.commit()
                sql1 = 'update 会议 set 当前人数=当前人数+' + '1' + ' where 会议id=' + mID + ';'
                cursor.execute(sql1)
                conn.commit()
                flash('参与成功')
            except:
                flash('数据库异常')
                conn.rollback()
    except:
        flash('数据库异常')
    return redirect(url_for('lookMeeting'))


# 删除会议
@view.route('/look_meeting/<meetingID>/', methods=['GET', 'POST'])
def deleteMeeting(meetingID):
    print(meetingID)
    conn = pymysql.connect(host="127.0.0.1", user="wprofessor", password="Aa*123456", database="DBMeeting",
                           charset="utf8")
    cursor = conn.cursor()
    sql = 'select 开始时间 from 会议 where 会议id=' + meetingID + ';'
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        if result[0][0] < todayDate:
            flash('会议正在进行，不能删除')
        else:
            sql = 'delete from 会议 where 会议id=' + meetingID + ';'
            sql1 = 'delete from 选会议表 where 会议id=' + meetingID + ';'

            try:
                cursor.execute(sql1)
                conn.commit()
                flash('删除成功')
            except:
                flash('数据库异常')
                conn.rollback()
            try:
                cursor.execute(sql)
                conn.commit()

            except:
                flash('数据库异常')
                conn.rollback()
    except:
        flash('数据库异常')
    cursor.close()
    conn.close()
    return redirect(url_for('lookMeeting'))


# 添加会议室
@view.route('/add_meetingroom/', methods=['GET', 'POST'])
def addMeetingRoom():
    form = wtf.appendMeeting()

    if request.method == 'POST':
        mrID = request.form.get('mrID')
        mrName = request.form.get('mrName')
        mrCapacity = request.form.get('mrCapacity')
        mrContent = request.form.get('mrContent')
        conn = pymysql.connect(host="127.0.0.1", user="wprofessor", password="Aa*123456", database="DBMeeting",
                               charset="utf8")
        print(mrID, mrName, mrCapacity, mrContent)
        cursor = conn.cursor()
        sql = "insert into 会议室(会议室id,会议室名字,会议室容量,说明) values (%s,%s,%s,%s);"
        try:
            cursor.execute(sql, [int(mrID), mrName, int(mrCapacity), mrContent])
            conn.commit()
            flash('添加成功')
        except:
            flash('添加失败，注意容量和id是数字')
            conn.rollback()
        cursor.close()
        conn.close()
    return render_template('add_meetingroom.html', form=form, name=session.get('name'))


# 判断时间是否冲突
def judge(stime, etime, timelist):
    if timelist:
        for row in timelist:
            if row[0] > etime or row[1] < stime:
                return True
            else:
                return False
    return True


# 添加会议
@view.route('/add_meeting/', methods=['GET', 'POST'])
def addMeeting():
    form = wtf.reservationMeeting()
    if request.method == 'POST':
        mID = request.form.get('mID')
        mName = request.form.get('mName')
        resPerson = request.form.get('resPerson')
        mrName = request.form.get('mrName')
        startTime = request.form.get('startTime')
        endTime = request.form.get('endTime')
        mContent = request.form.get('mContent')
        conn = pymysql.connect(host="127.0.0.1", user="wprofessor", password="Aa*123456", database="DBMeeting",
                               charset="utf8")
        cursor = conn.cursor()
        sqlIsExistMR = 'select 会议室id from 会议室 where 会议室名字 =  \'' + mrName + '\';'
        try:
            cursor.execute(sqlIsExistMR)
            result = cursor.fetchall()
            print(result)
            if result:
                sqlIsConflict = 'select 开始时间,结束时间 from 会议 where 会议名=\'' + mrName + '\';'
                try:
                    cursor.execute(sqlIsConflict)
                    resultTime = cursor.fetchall()
                    if judge(startTime, endTime, resultTime):
                        if startTime > endTime:
                            flash('请核对预约时间')
                        else:
                            sqlAddMeeting = 'insert into 会议(会议id,会议名,预订者id,会议室id,开始时间,结束时间,说明) values (%s,%s,%s,%s,%s,%s,%s);'
                            try:
                                cursor.execute(sqlAddMeeting,
                                               [mID, mName, resPerson, result[0][0], startTime, endTime, mContent])
                                conn.commit()
                                flash('奥利给')
                            except:
                                flash('添加失败')
                                conn.rollback()
                    else:
                        flash('该会议室在此时间段已被预约')
                except:
                    flash('会议表查询失败')
            else:
                flash('该会议室不存在')
                print('该会议室不存在')
        except:
            flash('查询会议室表失败')
        cursor.close()
        conn.close()
        print(mID, mName, resPerson, mrName, startTime, endTime, mContent)
    if session.get('account') == '111111':
        return render_template('add_meeting.html', form=form, name=session.get('name'))
    else:
        return render_template('add_meeting_user.html', form=form, name=session.get('name'))


# 查看选会议表里
@view.route('/lookselectmeeting/', methods=['GET', 'POST'])
def lookSelectMeeting():
    results = db.query.lookSMTable()
    results_user = []
    for row in results:
        tump = list(row)
        tump.append('删除')
        results_user.append(tump)
    return render_template('lookselectmeeting.html', results_user=results_user, name=session.get('name'))


# 删除此次选择
@view.route('/lookselectmeeting/<major1ID>/<major2ID>/', methods=['GET', 'POST'])
def deleteSelectMeeting(major1ID, major2ID):
    print(major1ID, major2ID)
    conn = pymysql.connect(host="127.0.0.1", user="wprofessor", password="Aa*123456", database="DBMeeting",
                           charset="utf8")
    cursor = conn.cursor()
    sql0 = 'select 开始时间 from 会议 where 会议id=' + major2ID + ';'
    try:
        cursor.execute(sql0)
        result = cursor.fetchall()
        if result[0][0] < todayDate:
            flash('会议正在进行，不能删除')
        else:
            sql = 'delete from 选会议表 where 用户id=' + major1ID + ' and 会议id=' + major2ID + ';'
            sql1 = 'update 会议 set 当前人数=当前人数-' + '1' + ' where 会议id=' + major2ID + ';'
            try:
                print(sql)
                cursor.execute(sql)
                cursor.execute(sql1)
                conn.commit()
                flash('删除成功')
            except:
                flash('数据库异常')
                conn.rollback()
                cursor.close()
                conn.close()
    except:
        flash('数据库异常')
        cursor.close()
        conn.close()

    return redirect(url_for('lookSelectMeeting'))


# 修改会议
@view.route('/update_meeting/', methods=['GET', 'POST'])
def updateMeeting():
    return render_template('update_meeting.html', name=session.get('name'))


# 登录
@view.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('pass')
        try:
            db = pymysql.connect(host="127.0.0.1", user="wprofessor", password="Aa*123456", database="DBMeeting",
                                 charset="utf8")
            cursor = db.cursor()
            sql = "SELECT 账号,密码 FROM 用户 WHERE 账号=%s"
            temp_form = [username]
            cursor.execute(sql, temp_form)
            result = cursor.fetchall()
            print(result)
            for row in result:
                t_name = row[0]
                t_pas = row[1]
                if t_name == username and t_pas == password:
                    sql = 'select 姓名 from 用户 where 账号=%s' + ';'
                    cursor.execute(sql, t_name)
                    session['name'] = cursor.fetchall()[0][0]
                    session['account'] = t_name
                    if t_name == '111111':
                        return render_template('index.html', name=session.get('name'))
                    else:
                        return render_template('index_user.html', name=session.get('name'))
                else:
                    flash('❌ 您的账号或密码错误')
                    return render_template('Login.html')
        except:
            flash('❌ 您的账号或密码错误')
            return render_template('Login.html')
        db.close()
    return render_template('Login.html')


class User:
    username = ""
    password = ""
    password_check = ""
    name = ""
    id = 0
    sex = ""
    part = ""
    tel = ""
    goal = ""


@view.route('/sign_in', methods=['GET', 'POST'])
def index2():
    if request.method == 'POST':
        # 获取表单数据
        # 获取表单数据
        username = request.form.get('username1')
        password1 = request.form.get('pass1')
        password2 = request.form.get('pass2')
        name1 = request.form.get('name1')
        id1 = request.form.get('id1')
        sex1 = request.form.get('sex1')
        part1 = request.form.get('part1')
        tel = request.form.get('tel')
        goal = request.form.get('goal')
        if password1 != password2:
            flash('❌ 两次输入密码不相同')
            # return render_template('Sign_in.html')
        elif len(password1) < 6 or len(password2) < 6:
            flash('❌ 输入密码少于六位')
            # return render_template('Sign_in.html')

        # 连接数据库
        try:
            db = pymysql.connect(host="127.0.0.1", user="wprofessor", password="Aa*123456", database="DBMeeting",
                                 charset="utf8")
            cursor = db.cursor()
            sql = """INSERT INTO 审批表(id, name, 账号, 密码, sex, 部门, 目的, 联系方式)
                values (%s, %s, %s, %s, %s, %s, %s ,%s)"""
            temp_form = [id1, name1, username, password1, sex1, part1, goal, tel]
            cursor.execute(sql, temp_form)
            db.commit()
            flash('✔ 注册成功')
            return redirect(url_for('login'))
        except:
            db.rollback()
            try:
                db = pymysql.connect(host='localhost', port=3306, user='root', passwd='yangaoru', db='poject',
                                     charset='utf8')
                cursor = db.cursor()
                sql2 = "SELECT 账号 FROM 用户 WHERE 账号=%s"
                temp_form2 = [username]
                cursor.execute(sql2, temp_form2)
                result = cursor.fetchall()
                for row in result:
                    t1 = row[0]
                if t1 == username:
                    flash('❌ 您的账号已被注册！')
                    print(t1, username)
                    # return render_template('Sign_in.html')
                else:
                    flash('❌ 您的ID已被注册！')
                    # return render_template('Sign_in.html')
                db.close()

            except:
                flash('❌ 您的ID已被注册！')
                db.close()
                return render_template('Sign_in.html')
        db.close()
    return render_template('Sign_in.html')


@view.route('/forget', methods=['GET', 'POST'])
def index3():
    if request.method == 'POST':
        username1 = request.form.get('username')
        id1 = request.form.get('id')
        new_password1 = request.form.get('new_pass')
        print(len(new_password1))
        try:
            db = pymysql.connect(host="127.0.0.1", user="wprofessor", password="Aa*123456", database="DBMeeting",
                                 charset="utf8")
            cursor = db.cursor()
            sql = "SELECT 账号,用户id FROM 用户 WHERE 账号 = %s"
            temp_form = [username1]
            cursor.execute(sql, temp_form)
            result = cursor.fetchall()
            for row in result:
                t_name = row[0]
                t_id = row[1]
            if t_name == username1 and str(t_id) == id1:
                sql1 = "UPDATE 用户 SET 密码=%s WHERE 账号=%s"
                if len(new_password1) < 6:
                    flash('❌ 您的新密码少于六位')
                    return render_template('Forget.html')
                temp_form1 = [new_password1, t_name]
                # cursor = db.cursor()
                cursor.execute(sql1, temp_form1)
                db.commit()
                flash('✔ 密码修改成功')
                return render_template('Login.html')
            else:
                flash('❌ 抱歉，您的ID和账号不匹配')
                return render_template('Forget.html')
        except:
            flash('❌ 抱歉，您的ID和账号不匹配')
            return render_template('Forget.html')
    return render_template('Forget.html')


# 会议室推荐
# 最后的data是列表返回值
@view.route('/recommendMRoom/', methods=['GET', 'POST'])
def recommendMR():
    real_result = []
    if request.method == 'POST':
        video1 = video2 = 0
        light1 = light2 = 0
        meeting_type1 = meeting_type2 = meeting_type3 = meeting_type4 = meeting_type5 = meeting_type6 = meeting_type7 = meeting_type8 = meeting_type9 = 0
        meeting_need1 = meeting_need2 = meeting_need3 = meeting_need4 = 0

        num = request.form.get('num')
        video = request.form.get('video')
        area = request.form.get('area')
        mic = request.form.get('mic_num')
        meeting_type = request.form.get('meeting_type')
        meeting_need = request.form.get('meeting_need_lel')
        light = request.form.get('meeting_light')

        if meeting_need == '0':
            meeting_need1 = 1
        elif meeting_need == '1':
            meeting_need2 = 1
        elif meeting_need == '2':
            meeting_need3 = 1
        else:
            meeting_need4 = 1

        if meeting_type == '0':
            meeting_type1 = 1
        elif meeting_type == '1':
            meeting_type2 = 1
        elif meeting_type == '2':
            meeting_type3 = 1
        elif meeting_type == '3':
            meeting_type4 = 1
        elif meeting_type == '4':
            meeting_type5 = 1
        elif meeting_type == '5':
            meeting_type6 = 1
        elif meeting_type == '6':
            meeting_type7 = 1
        elif meeting_type == '7':
            meeting_type8 = 1
        else:
            meeting_type9 = 1

        if int(video) == 1:
            video2 = 1
        else:
            video1 = 1

        if int(light) == 1:
            light2 = 1
        else:
            light1 = 1
            # 列表值data
        data = [area, num, mic, video1, video2, meeting_type1, meeting_type2, meeting_type3, meeting_type4,
                meeting_type5, meeting_type6, meeting_type7, meeting_type8, meeting_type9, meeting_need1, meeting_need2,
                meeting_need3, meeting_need4, light1,
                light2]
        print(data)
        result = recommend_algorithm.predict([int(i) for i in data])
        conn = pymysql.connect(host="127.0.0.1", user="wprofessor", password="Aa*123456", database="DBMeeting",
                               charset="utf8")
        cursor = conn.cursor()
        sql = 'select * from 会议室 where 会议室名字=%s' + ';'

        for temp in result:
            cursor.execute(sql, temp)
            real_result.append(cursor.fetchall()[0])
    if session.get('account') == '111111':
        return render_template('mrr.html', name=session.get('name'), real_result=real_result)
    else:
        return render_template('mrr_user.html', name=session.get('name'), real_result=real_result)


if __name__ == '__main__':
    view.run()
