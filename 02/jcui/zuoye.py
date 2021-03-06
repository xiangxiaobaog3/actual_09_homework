#encoding:utf-8
''
import random
import time

#装饰器,用于计算程序耗时
def time_consuming():
    def timess(func):
        start = time.time()
        func()
        end = time.time()
        print '用时:%.3fs' % (end-start)
        return
    return timess
'''
-----------------------------------------------------------------------------------------------------------------------------------------------------
#二分查找
二分法查找的基本算法是 在一个有序的list中判断元素是否在list中，比较方法主要是，将当前元素和list中间的数字进行比较，如果当前元素比中间的数字小，那就可以在list的前半段进行查找，如果比中间的元素大，那就可以在list的后半段查找，如果和中间的数字相同，那就意味已找到，按照这个思路（主要是变换在list中查找的开始位置start和结束位置end）直到找到相等的元素（找到），或者是直到变换后的start>end（没找到）

[1,3,5,6,8,9]中找到3
-----------------------------------------------------------------------------------------------------------------------------------------------------
'''
# num_list = [1,3,5,6,8,9]
@time_consuming()
def binary_search():
    num_list = [-1, 5, 6, 10, 23, 34, 123, 213, 344, 435, 65535]
    nums = int(raw_input("%s 请从列表中选择查找的数字:" % num_list))
    left = 0
    right = len(num_list)-1
    mid = len(num_list)/2
    while left <= right:
        if nums == num_list[mid] :
            print "您输入的数字:%s在列表的索引位置为:%s" % (nums,mid) ,
            break
        elif nums > num_list[mid]:
            left = mid + 1
            mid = mid + len(num_list[left:right])/2 + 1
        else :
            right = mid - 1
            mid = mid - len(num_list[left:right])/2  - 1
    else:
        print "您输入的数字:%s不在列表中" % nums ,

'''
二分查找优化版本
'''
@time_consuming()
def binary_search_two():
   num_list = [-1, 5, 6, 10, 23, 34, 123, 213, 344, 435, 65535]
   nums = int(raw_input("%s 请从列表中选择查找的数字:" % num_list))
   left = 0
   right = len(num_list)
   while True:
       if left <= right:
           mid = (left+right)/2
           if nums == num_list[mid]:
               print "您输入的数字:%s在列表的索引位置为:%s" % (nums,mid) ,
               break
           elif nums > num_list[mid]:
               left = mid + 1
           else:
               right = mid - 1
       else:
           print "您输入的数字:%s不在列表中" % nums ,


'''
#猜数字的游戏
'''

@time_consuming()
def guess_num():
    n = 0
    nums = random.randint(0,100)
    while True :
        guess = int(raw_input('请在0-100的数字中猜一个数:'))
        if guess >100 or guess < 0 :
            print "您输入的数字超出范围,请重新输入"
        else:
            if nums == guess:
                print "恭喜你猜对了!合计一共猜了%s次,猜错%s次" % (n,n-1) ,
                break
            elif guess > nums:
                print "您猜的数字太大了"
            else:
                print "您猜的数字太小了"
        n += 1


'''
-----------------------------------------------------------------------------------------------------------------------------------------------------
#随机抽取两面同学的作业
-----------------------------------------------------------------------------------------------------------------------------------------------------
'''
name_list = ['靳德瑞', '祁成', '鲍鹏飞', '佘朝辉', '常华伟', '崔佳', '赵云海', '谭帥','李续', '郭云飞', '周福成', '桑鹏亮','赵勇']
'''
#方法一
'''
num1 = random.randint(1,len(name_list)-1)
name1 = name_list[num1]
name_list.pop(num1)
num2 = random.randint(1,len(name_list)-1)
name2 = name_list[num2]
print "方法一:本次抽查%s,%s的作业" % (name1,name2)
'''
#方法二
'''
names = random.sample(name_list,2)
print "方法二:本次抽查%s,%s的作业" % (names[0],names[1])

'''
-----------------------------------------------------------------------------------------------------------------------------------------------------
#插入排序
    所谓插入排序法，就是检查第i个数字，如果在它的左边的数字比它大，进行交换，这个动作一直继续下去，直到这个数字的左边数字比它还要小，就可以停止了。插入排序法主要的回圈有两个变数：i和j，每一次执行这个回圈，就会将第i个数字放到左边恰当的位置去。
    插入排序对一个list进行排序的算法，主要思路是从list第一个元素开始，每遍历一个元素保证从第一个元素到当前元素是一个有序的（从小到大）
插入排序就在于在遍历第N个元素时（其前N-1个元素是有序的），需要查找第N个元素在第N-1个元素中的位置
查找位置的方法有很多，一般使用将当前遍历的元素M（第N个）依次和他前面的元素比较（第N-1个元素，N-2，。。。1），找到第一个比M小的元素，然后将M插入到找到的元素后面
-----------------------------------------------------------------------------------------------------------------------------------------------------
'''
'''
方法一
'''
@time_consuming()
def Insertion_sort1():
    num_list = [23,344,34,10,5,6,-1,213,65535,123,435,10]
    for x in range(0,len(num_list)):
        for y in range(0,x+1):   #每次插入的数据与新的序列中的数做比较
            if num_list[x] < num_list[y]:
                num_list[x],num_list[y] = num_list[y],num_list[x]
        # print num_list #调试用
    print "插入排序(升幂)",num_list ,

'''
方法二
'''
@time_consuming()
def Insertion_sort2():
    num_list = [23,344,34,10,5,6,-1,213,65535,123,435,10]
    for x in range(0,len(num_list)):
        for y in range(x+1,len(num_list)):   #每次插入的数据与新的序列中的数做比较
            if num_list[x] < num_list[y]:
                num_list[x],num_list[y] = num_list[y],num_list[x]
        # print num_list #调试用
    print "插入排序(降幂)",num_list ,


'''
-----------------------------------------------------------------------------------------------------------------------------------------------------
#选择排序 (请老师帮忙看下这个算法的写法是否正确,我是根据理解自己写的!!!)
    选择排序：比如在一个长度为N的无序数组中，在第一趟遍历N个数据，找出其中最小的数值与第一个元素交换，第二趟遍历剩下的N-1个数据，找出其中最小的数值与第二个元素交换......第N-1趟遍历剩下的2个数据，找出其中最小的数值与第N-1个元素交换，至此选择排序完成。
-----------------------------------------------------------------------------------------------------------------------------------------------------
'''
@time_consuming()
def Selection_sort():
    num_list = [23,344,34,10,5,6,-1,213,65535,123,435,10]

    for i in range(0,len(num_list)-1):  #循环次数
        index = i
        for x in range(i+1,len(num_list)):
            if num_list[index] > num_list[x]:   #找到最小的数
                index = x
        # print num_list[i],num_list[index] #调试用,为了查看对比的结果
        num_list[i],num_list[index] = num_list[index],num_list[i]   #将最小的数与当前队列第一个做交换
    print "选择排序",num_list ,


'''
-----------------------------------------------------------------------------------------------------------------------------------------------------
#冒泡排序
    它重复地走访过要排序的数列，一次比较两个元素，如果他们的顺序错误就把他们交换过来。走访数列的工作是重复地进行直到没有再需要交换，也就是说该数列已经排序完成
-----------------------------------------------------------------------------------------------------------------------------------------------------
'''
@time_consuming()
def Bubble_sort():
    num_list = [23,344,34,10,5,6,-1,213,65535,123,435,10]
    for x in range(0,len(num_list)-1):  #循环次数
        for y in range(0,len(num_list)-1-x):
            if num_list[y] > num_list[y+1]:    #每两个比较
                num_list[y],num_list[y+1] = num_list[y+1],num_list[y]    #对调

    print "冒泡排序",num_list ,


'''
-----------------------------------------------------------------------------------------------------------------------------------------------------
#其他排序(个人理解是冒泡排序)(请老师帮忙看下!!!)
-----------------------------------------------------------------------------------------------------------------------------------------------------
'''
@time_consuming()
def other_sort():
    num_list = [23,344,34,10,5,6,-1,213,65535,123,435,10]
    for i in range(0,len(num_list)):
        for j in range(i+1,len(num_list)):
            if num_list[i] > num_list[j]:
                num_list[i],num_list[j] = num_list[j],num_list[i]
    print "其他排序",num_list ,

'''
-----------------------------------------------------------------------------------------------------------------------------------------------------

-----------------------------------------------------------------------------------------------------------------------------------------------------
'''