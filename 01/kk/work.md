## 作业一 ##
一个序列
[1,2,3,2,12,3,1,3,21,2,2,3,4111,22,3333,444,111,4,5,777,65555,45,33,45]
求这个list的最大的两个值


找序列中最大的值
max_num = None
for  in  遍历序列
若发现max_num为None 咱们把当前遍历的元素赋值给max_num
若发现max_num不为None（肯定为数组）将max_num和当前遍历的元素进行比较, 如果当前元素比max_num大, max_num替换为当前遍历的元素

找第二个最大的元素
与找第一个最大值方法一样, 跳过max_num的值


## 作业二 ##
打印乘法口诀

1 * 1 = 1    1 * 2 = 2  1 * 3 = 3                                 1 * 9 = 9
2 * 1 = 2    2 * 2 = 4  2 * 3 = 6                                 2 * 9 = 18
3 * 1 = 3                                                         3 * 9 = 27
4 * 1 = 4
5 * 1 = 5
6
7
8
9                                                                 9 * 9 = 81


for i in range(1, 10):
    for j in range(1, 10):
        print '%s * %s = %s' % (i, j, (i * j)),
    print ''