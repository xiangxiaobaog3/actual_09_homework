#!/usr/bin/env python
#-*-coding: UTF-8 -*-
#表创建语句 create table access_logs (IP varchar(32) DEFAULT NULL, URL text DEFAULT NULL, CODE varchar(10) DEFAULT NULL, TOTAL int DEFAULT NULL) ENGINE=TokuDB DEFAULT CHARSET=utf8
import gconf
import MySQLdb
import time
from dbutils import execute_sql

path = gconf.ACCESS_LOG
log = {}	
rh = open(path,'r')
for rf in rh:
	x = (rf.split(' ')[0], rf.split(' ')[6], rf.split(' ')[8])
	log[x] = log.get(x,1) + 1
rh.close()

#方法一遍历插入数据
def insert_logs(log=log):
	conn = None
	cur = None
	count = 0
	try:
		conn = MySQLdb.connect(host=gconf.MYSQL_HOST, port=gconf.MYSQL_PORT, user=gconf.MYSQL_USER, passwd=gconf.MYSQL_PASSWORD, db=gconf.MYSQL_DB, charset=gconf.MYSQL_CHARSET)
		cur = conn.cursor()
		for i, ii in log.items():
			IP = i[0]
			URL = i[1]
			CODE = i[2]
			TOTAL = ii
			sql = 'insert into access_logs set IP=%s, URL=%s, CODE=%s, TOTAL=%s'
			args = (IP, URL, CODE, TOTAL)
			count = cur.execute(sql,args)
		conn.commit()
	except BaseException as e:
		print e
	finally:
		if cur:
			cur.close()
		if conn:
			conn.close()		

#方法二,使用load data导入数据			
def load_data():		
	wh = open('access_logs.txt', 'w')
	for i, ii in log.items():
		for iii in i:
			wh.write(iii)
			wh.write(",")
		wh.write(str(ii))	
		wh.write("\n")
	wh.close()	
	
	sql = 'load data local infile "access_logs.txt" into table access_logs fields terminated by "," lines terminated by "\n"'
	args = ()
	fetch = False
	execute_sql(sql, args, fetch)
	
def logscount(cut=10):
	rt_list = []
	sql = 'select * from access_logs order by TOTAL desc limit %s'
	args = cut
	count, rt_list = execute_sql(sql, args)
	return rt_list
	

if __name__ == '__main__':	
	start = time.clock()
	#print insert_logs()
	print load_data()
	end = time.clock()
	print end - start

