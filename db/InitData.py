#导入pumysql模块
import pymysql
#连接数据库
conn = pymysql.connect(host = "127.0.0.1",user = "wprofessor",password = "Aa*123456",database = "DBMeeting",charset = "utf8")

#得到一个可以执行Sql语句的光标对象
cursor = conn.cursor()

# sql1 = "insert into 用户(用户id,姓名,账号,密码,联系方式,性别,部门) values(88801,'李铁',81181,111111,'881801','男','财政部')"
# sql2 = "insert into 用户(用户id,姓名,账号,密码,联系方式,性别,部门)values(88802,'张丽',81182,222222,'881802','女','人力资源部')"
# sql3 = "insert into 用户(用户id,姓名,账号,密码,联系方式,性别,部门) values(88803,'王俊',81183,333333,'881803','男','行政部')"
#
# sql4 = "insert into 会议室(会议室id,会议室名字,会议室容量,说明) values(801,'梦竹轩',50,'')"
# sql5 = "insert into 会议室(会议室id,会议室名字,会议室容量,说明) values(802,'红莲居',100,'')"
# sql6 = "insert into 会议室(会议室id,会议室名字,会议室容量,说明) values(803,'祥瑞苑',100,'')"
# sql7 = "insert into 会议室(会议室id,会议室名字,会议室容量,说明) values(804,'好事堂',300,'')"
#
# sql8 = "insert into 会议(会议id,会议名,预订者id,会议室id,当前人数,开始时间,结束时间,说明) values(8801,'人事调动',88801,802,33,'2020/01/06','2020/01/08','')"
# sql9 = "insert into 会议(会议id,会议名,预订者id,会议室id,当前人数,开始时间,结束时间,说明) values(8802,'工资调整',88802,803,2,'2020/01/07','2020/01/09','')"
# sql10 = "insert into 会议(会议id,会议名,预订者id,会议室id,当前人数,开始时间,结束时间,说明) values(8803,'公司聚会',88803,804,12,'2020/01/05','2020/01/06','')"
#
# sql11 = "insert into 选会议表(用户id,会议室id,会议id,会议名) values(88801,802,8801,'人事调动')"
# sql12 = "insert into 选会议表(用户id,会议室id,会议id,会议名) values(88802,803,8802,'工资调整')"
# sql13 = "insert into 选会议表(用户id,会议室id,会议id,会议名) values(88803,804,8803,'公司聚会')"
#
# sql14 = "insert into 审批表(id,name,sex,联系方式,目的) values(1,'王佳豪','男','1835654565','新人加入，公司见面会')"
# sql15 = "insert into 审批表(id,name,sex,联系方式,目的) values(2,'董倬君','女','1354353463','向员工宣布上调工资')"
# sql16 = "insert into 审批表(id,name,sex,联系方式,目的) values(3,'刘川瑜','男','1454323443','筹备公司聚会内容')"
# sql17 = "insert into 审批表(id,name,sex,联系方式,目的) values(4,'杨敖儒','男','1245334332','筹备公司聚会内容')"

#
# cursor.execute(sql1)
# cursor.execute(sql2)
# cursor.execute(sql3)
# cursor.execute(sql4)
# cursor.execute(sql5)
# cursor.execute(sql6)
# cursor.execute(sql7)
# cursor.execute(sql8)
# cursor.execute(sql9)
# cursor.execute(sql10)
# cursor.execute(sql11)
# cursor.execute(sql12)
# cursor.execute(sql13)
# cursor.execute(sql14)
# cursor.execute(sql15)
# cursor.execute(sql16)
# cursor.execute(sql17)
#提交事务
conn.commit()
#关闭光标对象
cursor.close()
#关闭数据库连接
conn.close()