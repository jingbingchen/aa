counter = 100  # 赋值整型变量
miles = 1000.0  # 浮点型
name = "John"  # 字符串

print(counter)
print(miles)
print(name)

#python的列表
#List（列表） 是 Python 中使用最频繁的数据类型。
#列表可以完成大多数集合类的数据结构实现。它支持字符，数字，字符串甚至可以包含列表（即嵌套）。
#列表用 [ ] 标识，是 python 最通用的复合数据类型。
#列表中值的切割也可以用到变量 [头下标:尾下标] ，就可以截取相应的列表，从左到右索引默认 0 开始，从右到左索引默认 -1 开始，下标可以为空表示取到头或尾。

list = ['runoob', 786, 2.23, 'john', 70.2]
tinylist = [123, 'john']

print(list)  # 输出完整列表
print(list[0])  # 输出列表的第一个元素
print(list[1:3])  # 输出第二个至第三个元素
print(list[2:])  # 输出从第三个开始至列表末尾的所有元素
print(tinylist * 2)  # 输出列表两次
print(list + tinylist)  # 打印组合的列表

#python的元组
#元组是另一个数据类型，类似于 List（列表）。
#元组用 () 标识。内部元素用逗号隔开。但是元组不能二次赋值，相当于只读列表
tuple = ('runoob', 786, 2.23, 'john', 70.2)
tinytuple = (123, 'john')

print
tuple  # 输出完整元组
print
tuple[0]  # 输出元组的第一个元素
print
tuple[1:3]  # 输出第二个至第四个（不包含）的元素
print
tuple[2:]  # 输出从第三个开始至列表末尾的所有元素
print
tinytuple * 2  # 输出元组两次
print
tuple + tinytuple  # 打印组合的元组


#以下是元组无效的，因为元组是不允许更新的。而列表是允许更新的
tuple = ( 'runoob', 786 , 2.23, 'john', 70.2 )
list = [ 'runoob', 786 , 2.23, 'john', 70.2 ]
tuple[2] = 1000    # 元组中是非法应用
list[2] = 1000     # 列表中是合法应用

'''
Python 字典
字典(dictionary)是除列表以外python之中最灵活的内置数据结构类型。列表是有序的对象集合，字典是无序的对象集合。
两者之间的区别在于：字典当中的元素是通过键来存取的，而不是通过偏移存取。
字典用"{ }"标识。字典由索引(key)和它对应的值value组成。
'''
dict = {}
dict['one'] = "This is one"
dict[2] = "This is two"

tinydict = {'name': 'john', 'code': 6734, 'dept': 'sales'}

print(dict['one'])  # 输出键为'one' 的值
print
dict[2]  # 输出键为 2 的值
print
tinydict  # 输出完整的字典
print
tinydict.keys()  # 输出所有键
print
tinydict.values()  # 输出所有值

#python的运算符
