import pymysql
import time

todayDate = time.strftime("%Y-%m-%d", time.localtime())




# 查询用户
def selectUser():
    conn = pymysql.connect(host="127.0.0.1", user="wprofessor", password="Aa*123456", database="DBMeeting",
                           charset="utf8")
    cursor = conn.cursor()
    sql = 'select * from 用户'
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
    except:
        print("查询用户表失败")
    conn.close()
    return results


# 我的预定
def myReservation(ID1):
    conn = pymysql.connect(host="127.0.0.1", user="wprofessor", password="Aa*123456", database="DBMeeting",
                           charset="utf8")
    cursor = conn.cursor()
    sql = "select 会议名,会议室名字,开始时间,结束时间 " \
          "from 会议,会议室 " \
          "where 会议.会议室id = 会议室.会议室id AND 预订者id = %s"
    # 此处的条件不可直接用ID1放入，需间接放入变量
    try:
        cursor.execute(sql, (ID1))
        results = cursor.fetchall()
    except:
        print("查询我的预定失败")
    cursor.close()
    conn.close()
    return results


# 我的会议
def myMeeting(ID2):
    conn = pymysql.connect(host="127.0.0.1", user="wprofessor", password="Aa*123456", database="DBMeeting",
                           charset="utf8")
    cursor = conn.cursor()
    sql = "select 选会议表.会议id,选会议表.会议名,会议室名字,开始时间,结束时间 " \
          "from 会议,会议室,选会议表 " \
          "where 选会议表.会议室id = 会议室.会议室id AND 选会议表.会议id = 会议.会议id AND 选会议表.用户id = %s;"
    try:
        cursor.execute(sql, (ID2))
        results = cursor.fetchall()
    except:
        print("查询我的会议失败")
    cursor.close()
    conn.close()
    return results


def judge(timeList):
    for time in timeList:
        if time[0] <= todayDate and time[1] >= todayDate:
            return True
    return False


# 查看会议室
def lookMeetingRoom():
    conn = pymysql.connect(host="127.0.0.1", user="wprofessor", password="Aa*123456", database="DBMeeting",
                           charset="utf8")
    cursor = conn.cursor()
    sql = 'select * from 会议室;'
    new_results = []
    try:
        cursor.execute(sql)
        results = cursor.fetchall()

        for i in results:
            new_results.append(list(i))
    except:
        print('查询会议室表失败')
    for row in range(len(results)):
        sql = 'select 开始时间,结束时间 from 会议 where 会议室id = ' + str(results[row][0]) + ';'
        try:
            cursor.execute(sql)
            timeList = cursor.fetchall()
            if timeList:
                if judge(timeList):
                    new_results[row][3] = 1
                else:
                    new_results[row][3] = 0
            else:
                new_results[row][3] = 0
        except:
            print('查询失败')

    cursor.close()
    conn.close()
    return new_results


# 查看会议
def loolMeeting():
    conn = pymysql.connect(host="127.0.0.1", user="wprofessor", password="Aa*123456", database="DBMeeting",
                           charset="utf8")
    cursor = conn.cursor()
    sql = 'delete from 会议 where 结束时间 <' + todayDate + ';'
    try:
        cursor.execute(sql)
        conn.commit()
    except:
        conn.rollback()
    sql = 'select * from 会议;'
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
    except:
        print('查看会议表失败')
    cursor.close()
    conn.close()
    return results


# 注册审批
def lookAllRegister():
    conn = pymysql.connect(host="127.0.0.1", user="wprofessor", password="Aa*123456", database="DBMeeting",
                           charset="utf8")
    cursor = conn.cursor()
    sql = 'select id,name,sex,目的 from 审批表;'
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
    except:
        print("查询审批表失败")
    cursor.close()
    conn.close()
    return results


# 查看选会议表
def lookSMTable():
    conn = pymysql.connect(host="127.0.0.1", user="wprofessor", password="Aa*123456", database="DBMeeting",
                           charset="utf8")
    cursor = conn.cursor()
    sql = 'select * from 选会议表;'
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
    except:
        print("查询选会议表失败")
    cursor.close()
    conn.close()
    return results


print(lookSMTable())
