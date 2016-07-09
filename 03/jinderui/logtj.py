# encoding: utf-8

d = {}
'''
打开文件把数据读入到字典里面用ip,url,返回值组成元组作为key。
先把所有key赋空值，发现key在字典里面就把value加1。直到循环完成
'''
with open('nginx.log','r') as f:
    for linelist in [line.strip().split(' ') for line in f]:
        dfile = linelist[0],linelist[6],linelist[8]
        d[dfile] = d.setdefault(dfile,0) + 1

# 把生成的字典转换成列表
dl = d.items()

# 利用冒泡排序算法对列表进行排序
for num in range(len(dl)):
    for num in range(len(dl) - 1 - num):
        if dl[num][1] > dl[num+1][1]:
            dl[num],dl[num+1] = dl[num+1],dl[num]

# 取top10
for x in dl[-1:-11:-1]:
    print "ip:{ip}  url:{url}  state:{state}  num:{num}".format(ip=x[0][0],url=x[0][1],state=x[0][2],num=x[1])

'''
功能ok,加油
改进:
1. line13, 既然已经在line12设置的默认值，那此处是不是只用+=1就ok了呢
'''
