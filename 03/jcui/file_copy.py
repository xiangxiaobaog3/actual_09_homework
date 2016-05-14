#encoding:utf-8

import time

def time_consuming():
    def timess(func):
        start = time.time()
        func()
        end = time.time()
        print '用时:%.3fs' % (end-start)
        return
    return timess



@time_consuming()
def copy_file():
    sptah='f:\\360yunpan.zip'
    dpath='f:\\testcopy.zip'
    sfile = open(sptah,'rb')
    dfile = open(dpath,'wb')
    while True:
        data = sfile.read(4096)
        if len(data) == 0:
            sfile.close()
            dfile.close()
            print '复制文件完毕,原文件:%s,目的文件:%s' % (sfile.name,dfile.name),
            break
        else:
            dfile.writelines(data)
