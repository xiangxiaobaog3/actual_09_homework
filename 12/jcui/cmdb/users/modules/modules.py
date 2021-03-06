#encoding:utf-8
import json
import string
from random import choice
from functools import wraps

import time
import datetime

import paramiko

from dbutils import MySQLConnection as SQL
from dbutils import md5_str
from flask import session,redirect

class User(object):

    def __init__(self,username,password,age,telphone,email):
        self.id = id
        self.username = username
        self.password = password
        self.age = age
        self.telphone = telphone
        self.email = email
    @classmethod
    # 定义装饰器函数,为了检查是否处于登陆状态
    def login_check(cls,func):
        @wraps(func)  # 为了解决python多装饰器出现的bug
        def check(*args, **kwargs):
            if session.get('username') is None:
                return redirect('/')
            rt = func(*args, **kwargs)
            return rt  # 返回函数的值

        return check  # 返回内层函数的结果

    @classmethod
    def validate_login(cls,username, password):
        _columns  = ('id','username')
        _sql = 'select * from user where username = %s and password = %s'
        args = (username, md5_str(password))
        sql_count, rt_list = SQL.excute_sql(_sql, args)
        return dict(zip(_columns,rt_list[0])) if sql_count != 0 else None


    @classmethod
    def get_list(cls):
        colloens = ('id', 'username', 'password', 'age', 'telphone', 'email')
        _sql = 'select * from user'
        rt = []
        sql_count, rt_list = SQL.excute_sql(_sql)  # 函数调用
        for i in rt_list:
            rt.append(dict(zip(colloens, i)))
        return rt

    @classmethod
    def get_alone_user(cls,id):
        users = cls.get_list()
        return [i for i in users if i.get('id') == id ]

    @classmethod
    def user_add(cls,params):
        username = params.get('username')
        password = params.get('password')
        age = params.get('age')
        telphone = params.get('telphone')
        email = params.get('email')
        _sql_select = 'select * from user where username = %s'
        _sql_insert = 'insert into user(username,password,age,telphone,email) values(%s,%s,%s,%s,%s)'
        agrs1 = (username,)
        _sql_count, rt_list = SQL.excute_sql(_sql_select, agrs1)
        if _sql_count != 0:
            return False, username + '已存在,请尝试其他的名字'
        args2 = (username, md5_str(password), age, telphone, email)
        SQL.excute_sql(_sql_insert, args2)
        return True, '添加成功'

    @classmethod
    def user_update(cls,params):
        username = params.get('username')
        id = params.get('id')
        age = params.get('age')
        telphone = params.get('telphone')
        email = params.get('email')
        _sql = 'update user set age=%s ,telphone=%s ,email=%s where id=%s and username=%s'
        args = (age, telphone, email, id, username)
        _sql_count, rt_list = SQL.excute_sql(_sql, args)
        if _sql_count != 0:
            return True, '更新成功'
        return False, '更新失败'

    @classmethod
    def user_del(cls,id, username):
        _sql = 'delete from user where id=%s and username=%s'
        args = (id, username)
        _sql_count, rt_list = SQL.excute_sql(_sql, args)
        if _sql_count != 0:
            return True
        return False

    @classmethod
    def valid_change_passwd(cls,uid, upass, muser, mpass):
        if not cls.validate_login(muser, mpass):
            return False, '管理员密码错误'
        if cls.get_alone_user(uid):  # 逻辑有问题,需要看
            return False, '用户不存在'
        if len(upass) < 6:
            return False, '密码长度小于6个字符'
        return True, '验证成功'

    @classmethod
    def change_passwd(cls,uid, upass):
        _sql = 'update user set password = %s where id = %s'
        _args = (md5_str(upass), uid)
        _sql_count, rt_list = SQL.excute_sql(_sql, _args)
        if _sql_count:
            return True, '修改成功'
        return False, '修改失败'

    @classmethod
    def user_reset(cls,id, username):
        _sql = 'update user set password = %s where id=%s and username=%s'
        newpassword = ''.join([choice(string.ascii_letters + string.digits) for i in range(8)])
        args = (md5_str(newpassword), id, username)
        _sql_count, rt_list = SQL.excute_sql(_sql, args)
        if _sql_count != 0:
            return True, '重置成功', newpassword
        return False, '重置失败', newpassword

    @classmethod
    def validate_mpass(cls,params):
        mgrpass = params.get('mgrpass')
        mgruser = 'admin'
        ip = params.get('ip')
        cmd = params.get('cmd').split('\n')
        _sql = 'select * from user where username=%s and password=%s'
        _args = (mgruser,md5_str(mgrpass))
        _sql_count,rt_list = SQL.excute_sql(_sql,_args)
        if _sql_count != 0 :
            _ssh = Ssh_cmd(ip,cmd)
            return _ssh.ssh_cmd()
        return False,'管理员密码验证失败'

class Ssh_cmd(object):
    def __init__(self,ip,cmd=[]):
        self.ip = ip
        self.cmd = cmd
        self.username = 'op'
        self.password = 'qingdao0613'
        self.port = 22
        self._ssh = None
        self.__conn()

    def __conn(self):
        try:
            self._ssh = paramiko.SSHClient()
            self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self._ssh.connect(self.ip, self.port, self.username,self.password)
        except BaseException as e:
            return False,e

    def ssh_cmd(self):
        _rt_list = []
        if self._ssh:
            for _cmd in self.cmd:
                stdin, stdout, stderr = self._ssh.exec_command(_cmd.strip('\r'))
                # _rt_list.append([_cmd, stdout.readlines(), stderr.readlines()])
                _rt_list.append([stdout.readlines(), stderr.readlines()])

            self._ssh.close()
            return True,_rt_list
        return False,'执行失败'


    def ssh_sftp(self):
        pass


class Logs(object):
    @classmethod
    def log_anslysis(cls,sfile):
        file_dict = {}
        try:
            files = open(sfile, 'r')
            for i in files:
                i = i.split()
                x, y, z = i[0], i[6], i[8]
                file_dict[(x, y, z)] = file_dict.get((x, y, z), 0) + 1
        except BaseException as e:
            print e
            return ''
        finally:
            if files:
                files.close()
        return [(x[0][0],x[0][1],x[0][2],x[1]) for x in sorted(file_dict.items(), key=lambda x: x[1], reverse=False) ]

    @classmethod
    def logs_import_sql(cls,logs_path):
        # logs_path = '/home/op/test/www_access_20140823.log'
        # logs_path = '/home/jcui/files/www_access_20140823.log'
        log_list = cls.log_anslysis(logs_path)
        print log_list
        _sql = 'insert into access_logs(ip,url,code,nums) values(%s,%s,%s,%s)'
        if SQL.excute_log_sql(_sql, log_list):
            return True
        return False

    @classmethod
    def log_access(cls,top=10):
        colloens = ('id', 'ip', 'url', 'code', 'nums')
        _sql = 'select * from access_logs order by nums desc limit %s'
        args = (top,)
        rt = []
        _sql_count, rt_list = SQL.excute_sql(_sql, args)
        for x in rt_list:
            rt.append(dict(zip(colloens, x)))
        return rt

    @classmethod
    def log_code_list(cls):
        _sql = 'select code,sum(nums) from access_logs group by code'
        _sql_count,_rt_list = SQL.excute_sql(_sql)
        _code_list = []
        all_code = 0
        if _sql_count != 0:
            for _code,_nums in _rt_list:
                all_code += _nums
            for _code,_nums in _rt_list:
                rt = {}
                rt['name'] = _code
                rt['y'] = round(_nums/all_code,2)
                _code_list.append(rt)
            return _code_list
        return []

    @classmethod
    def log2_code_list(cls):
        _sql = 'select status,count(status) from access_logs2 group by status'
        _cnt,_rt_list = SQL.excute_sql(_sql)
        status_legend = []
        status_data = []
        _code_list = []
        if _cnt != 0:
            for _status,_count in _rt_list:
                status_legend.append(_status)
                status_data.append({'name':_status,'value':_count})
            return status_legend, status_data
        return [],[]

    @classmethod
    def log2_time_status(cls):
        _sql = 'select date_format(logtime,"%%Y-%%m-%%d %%H:00:00"),status,count(*) from access_logs2 where logtime >= %s group by logtime,status;'
        _last_time = time.strftime('2014-08-%d %H:%M:%S',time.localtime(time.time() - 4 * 24 * 60 * 60))          #最近24小时的
        _cnt,_rt_list = SQL.excute_sql(_sql,(_last_time,))

        _legends = []
        _times = []
        _datas = []
        _temp_dict = {}
        for _time ,_status ,_cnt in _rt_list:
            if _status not in _legends:
                _legends.append(_status)
            if _time not in _times:
                _times.append(_time)
            _temp_dict.setdefault(_status,{})
            _temp_dict[_status][_time] = _cnt

        for _status,_stat in _temp_dict.items():
            _node = {
                'name': _status,
                'type': 'bar',
                'barWidth':30,
                'stack':'web_time_code',
                'data':[_stat.get(x,0) for x in _times]
            }
            _datas.append(_node)

        return _legends,_times,_datas

    @classmethod
    def log2_map(cls):
        _sql = 'select city,lat,lng,count(city) from access_logs2 group by city,lat,lng;'
        _server_ip = '211.151.99.93'
        _server_addr = '北京'
        _server_lat = '	117.10'
        _server_lng = '40.13'
        _cnt,_rt_list = SQL.excute_sql(_sql)
        _map_geocoord = {}
        _map_markline = []
        _map_markpoint = []
        if _cnt != 0:
            for _city,_lat,_lng,_nums in _rt_list:
                _map_geocoord[_city] = [_lng,_lat]
                _map_markline.append([{'name':_city,'value':_nums},{'name':_server_addr}])
                _map_markpoint.append({'name':_city,'value':_nums})
            # print _map_geocoord
            # print _map_markline
            # print _map_markpoint
            _map_geocoord[_server_addr] = [_server_lat,_server_lng]
            #
            # _map_geocoord = {
            #     '上海': [121.4648, 31.2891],
            #     '北京': [116.4551, 40.2539],
            #     '大连': [122.2229, 39.4409],
            #     '广州': [113.5107, 23.2196]
            # }

            # _map_markline = [
            #     [{"name": '上海', "value": 95}, {"name": '北京'}],
            #     [{"name": '广州', "value": 90}, {"name": '北京'}],
            #     [{"name": '大连', "value": 80}, {"name": '北京'}]
            # ]
            #
            # _map_markpoint = [
            #     {"name": '上海', "value": 95},
            #     {"name": '广州', "value": 90},
            #     {"name": '大连', "value": 80}
            # ]

            return _map_geocoord,_map_markline,_map_markpoint
        return [],[],[]

class Assets(object):

    def __init__(self,id,sn,ip,hostname,os,cpu,ram,disk,idc_id,admin,business,purchase_date,warranty,vendor,model,status):
        self.id = id
        self.sn = sn
        self.ip = ip
        self.hostname = hostname
        self.os = os
        self.cpu = cpu
        self.ram = ram
        self.disk = disk
        self.idc_id = idc_id
        self.admin = admin
        self.business = business
        self.purchase_date = purchase_date
        self.warranty = warranty
        self.vendor = vendor
        self.model = model
        self.status = status
    @classmethod
    def get_list(cls):
        _column = 'id,sn,ip,hostname,os,cpu,ram,disk,idc_name,admin,business,purchase_date,warranty,vendor,model,status'
        _columns = _column.split(',')
        _sql = 'select {column} from assets,idc_name where assets.status=0 and assets.idc_id = idc_name.idc_id;'.format(column=_column)
        _cnt,_rt_list = SQL.excute_sql(_sql)
        return [dict(zip(_columns,i)) for i in _rt_list ]

    @classmethod
    def get_by_id(cls,aid):
        _column = 'id,sn,ip,hostname,os,cpu,ram,disk,idc_id,admin,business,purchase_date,warranty,vendor,model,status'
        # _sql = 'select {coll} from assets,idc_name where assets.status=0 and assets.idc_id = idc_name.idc_id and id = %s'.format(coll=_column)
        _sql = 'select {coll} from assets where id = %s'.format(coll=_column)
        _args = (aid,)
        _cnt, _rt_list = SQL.excute_sql(_sql, _args)
        rt = []
        if _cnt != 0:
            for x in range(len(_column.split(','))):
                if _column.split(',')[x] == 'purchase_date':
                    rt.append((_column.split(',')[x], _rt_list[0][x].strftime("%Y-%m-%d")))
                    continue
                rt.append((_column.split(',')[x], _rt_list[0][x]))
            return dict(rt)
        return ''

    @classmethod
    def get_idc_name(cls):
        _sql = 'select idc_id,idc_name from idc_name'
        rt = []
        _cnt, _rt_list = SQL.excute_sql(_sql)
        for i in _rt_list:
            rt.append(i)
        return rt

    @classmethod
    def delete(cls,id):
        _sql = 'update assets set status = 1 where id=%s'
        _args = (id,)
        _cnt, _rtlist = SQL.excute_sql(_sql, _args)
        if _cnt != 0:
            return True, '删除成功'
        return False, '删除失败'

    @classmethod
    def ip_check(cls,ip):
        q = ip.split('.')
        return len(q) == 4 and len(filter(lambda x: x >= 0 and x <= 255, \
                                          map(int, filter(lambda x: x.isdigit(), q)))) == 4

    @classmethod
    def validate_create(cls,params):
        collent = params.keys()
        result = {}
        for i in collent:
            if params[i] == '':
                result[i] = '%s 不能为空' % i
        # 检查SN的唯一
        sn = params.get('sn').strip()
        if len(sn) >= 6:
            _sql = 'select * from assets where sn = %s and status = 0'
            _args = (sn,)
            _cnt, rt_list = SQL.excute_sql(_sql, _args)
            if _cnt != 0:
                result['sn'] = 'SN编码已存在'
        else:
            result['sn'] = 'SN编码太短'

        # 检查IP的唯一
        ip = params.get('ip').strip()
        if cls.ip_check(ip):
            _sql = 'select * from assets where ip = %s and status = 0'
            _args = (ip,)
            _cnt, rt_list = SQL.excute_sql(_sql, _args)
            if _cnt != 0:
                result['ip'] = 'IP地址已存在'
        else:
            result['ip'] = 'IP地址不合法'

        # 检查主机名的唯一
        hostname = params.get('hostname').strip()
        _sql = 'select * from assets where hostname = %s and status = 0'
        _args = (hostname,)
        _cnt, rt_list = SQL.excute_sql(_sql, _args)
        if _cnt != 0:
            result['hostname'] = '主机名已存在'

        if not result:
            return cls.create(params)
        return False, result.values()

    @classmethod
    def create(cls,params):
        _collent = []
        _values = []
        for k, v in params.items():
            _collent.append(k)
            _values.append(v)
        _sql = 'insert into assets({coll}) values%s'.format(coll=','.join(_collent))
        _args = (tuple(_values),)
        # print tuple(_values)
        _cnt, _rtlist = SQL.excute_sql(_sql, _args)
        if _cnt != 0:
            return True, '添加成功'
        return False, '入库失败'

    @classmethod
    def validate_update(cls,params):
        collent = params.keys()
        result = {}
        for i in collent:
            if params[i] == '':
                result[i] = '%s 不能为空' % i
        if not result:
            return cls.update(params)
        return False, result.values()

    @classmethod
    def update(cls,params):
        _column = 'sn,ip,hostname,os,cpu,ram,disk,idc_id,admin,business,purchase_date,warranty,vendor,model'
        id = params.get('id')
        rt_set = []
        _args = []
        for i in _column.split(','):
            # rt_set.append(i+'='+'\'%s\'' % params[i])               #预处理的方式是不需要加''的
            rt_set.append('{collens}=%s'.format(collens=i))
            _args.append(params.get(i))
        _args.append(id)
        _sql = 'update assets set {coll} where id = %s'.format(coll=','.join(rt_set))
        # _args = (id,)
        _cnt, _rtlist = SQL.excute_sql(_sql, _args)
        if _cnt != 0:
            return True, '更新成功'
        return False, '更新失败'


class Performs(object):

    @classmethod
    def add(cls,req):
        _ip = req.get('ip')
        _cpu = req.get('cpu')
        _ram = req.get('ram')
        _time = req.get('time')
        _sql = 'insert into performs(ip,cpu,ram,time) VALUES (%s,%s,%s,%s)'
        SQL.excute_sql(_sql,(_ip,_cpu,_ram,_time),False)
    @classmethod
    def get_list(cls,ip):
        _sql = 'select cpu,ram,time from performs where ip=%s and time >=%s ORDER by time asc'
        _args = (ip,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time() - 60*30)))
        _cnt,_rt_list = SQL.excute_sql(_sql,_args)
        if _cnt != 0:
            cpu_list = []
            ram_list = []
            time_list = []
            for _cpu,_ram,_time in _rt_list:
                cpu_list.append(round(_cpu,2))
                ram_list.append(round(_ram,2))
                time_list.append(_time.strftime('%H:%M'))
            return time_list,cpu_list,ram_list
        return False,'',''



    if __name__ == '__main__':
        pass