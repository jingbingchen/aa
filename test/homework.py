#判断是不是闰年
print("请输入你的年份")
year = int(input())
if (year%4==0) and (year%100 !=0) or (year%400==0):
    print("是闰年")
else:
    print("不是闰年")


#记录一周记账功能
money=float(input("请输入你第一天的账单：\n"))
money1=float(input("请输入你第二天的账单：\n"))
money2=float(input("请输入你第三天的账单: \n"))
money3=float(input("请输入你第四天的账单：\n"))
money4=float(input("请输入你第五天的账单：\n"))
money5=float(input("请输入你第六天的账单：\n"))
money6=float(input("请输入你第七天的账单：\n"))

#创建一个空列表
l=list()

l.append(money)
l.append(money1)
l.append(money2)
l.append(money3)
l.append(money4)
l.append(money5)
l.append(money6)

print('这是你这一星期的账单:')

for i in l:
    print('每天的账单:'+str(i)+'元')

total=money+money1+money2+money3+money4+money5+money6
print('这一星期一共消费：'+str(total)+'元')




#创建一个字典
bank={
    'user':['Alice','jack'],
    'password':['123','123'],
    'money':[10000,20000]
}

#循环
while True:
    name=str(input("欢迎登陆ATM机系统！请输入您的名字：\n"))
    if name in bank['user']:
        user_index=bank['user'].index(name)
        while True:
            password=str(input("请输入您的密码：\n"))
            if password in bank['password']:
                print("登陆成功")
                break
            else:
                print("您输入的密码不正确")
        break
    else:
        print("您输入的用户不存在")


while True:
    print('请选择以下业务:1.存款,2.取款,3.查询余额,4.取卡')
    operate=int(input())

    #存款
    if operate==1:
        depost=int(input("请输入您的存款金额:\n"))
        if depost<0:
            print("您你输入的存款金额必须要大于0")
        else:
            bank['money'][user_index]=int(bank['money'][user_index])+depost
            print("您的当前金额为:",bank['money'][user_index])
    #取款
    elif operate==2:
          withdrawal=int(input("请输入您要取款的金额\n"))
          if withdrawal >0 and withdrawal<bank['money'][user_index]:
              bank['money'][user_index]=int(bank['money'][user_index])-withdrawal
              print("您当前剩余余额：",bank['money'][user_index])
          else:
              print("您的余额不足")

    #查询余额
    elif operate==3:
            print('您的余额：',bank['money'][user_index])

    #退卡
    elif operate==4:
        print("您的卡已经退出，请收好您的卡")
        break

