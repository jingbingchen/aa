list1 = ['physics', 'chemistry', 1997, 2000]

print(list1)
del list1[2]
print("After deleting value at index 2 : ")
print(list1)


import msvcrt, sys, os
#定义用星号隐藏密码输入的函数
def psw_input():
    li = []
    while True:
        ch = msvcrt.getch()
        #回车
        if ch == b'\r':
            msvcrt.putch(b'\n')
            break
        #退格
        elif ch == b'\x08':
            if li:
                li.pop()
                msvcrt.putch(b'\b')
                msvcrt.putch(b' ')
                msvcrt.putch(b'\b')
        #Esc
        elif ch == b'\x1b':
            break
        else:
            li.append(ch)
            msvcrt.putch(b'*')
    return li

#定义CSDN银行ATM欢迎界面的函数
def ATM():
    '''
    CSDN银行ATM欢迎界面的函数
    '''
    print("="*14,"Bank of CSDN","="*14,"\n")
    print("{:^42}".format("ATM"),"\n")
    print("="*14,"Bank of CSDN","="*14,"\n")

#CSDN银行用户列表信息，用户信息包含：姓名、余额、密码（6位）、银行卡号（19位）
user_list = [{"name":"张  三","balance":10000,"password":"000000","numbers":"0000000000000000000"},
{"name":"李  四","balance":20000,"password":"111111","numbers":"1111111111111111111"},
{"name":"王  五","balance":30000,"password":"222222","numbers":"2222222222222222222"}]

#定义验证银行卡号与密码匹配的函数
def check(user_name,user_password):
    '''
    验证银行卡号与密码匹配的函数
    '''
    for i in range(len(user_list)):
        if user_name == user_list[i]["numbers"] and user_password == user_list[i]["password"]:
            return i #银行卡号与密码匹配则返回该用户在ATM系统内的ID值，否则返回None值

#定义用户登录成功后操作界面的函数
def interface():
    '''
    用户登录成功后操作界面的函数
    '''
    print("="*14,"用户操作界面","="*14,"\n")
    print("{0:2} {1:12} {2:12} {3:12}".format("  ","1. 查询","2. 取款","3. 存款"),"\n")
    print("{0:2} {1:10} {2:12}".format("  ","4. 修改密码","5. 退出"),"\n")
    print("="*42,"\n")

#定义用户查询信息的函数
def inquire(user_id):
    '''
    用户查询信息的函数
    '''
    print("="*14,"账号查询界面","="*14,"\n")
    print("|{0:<4}|{1:<18}|{2:<9}|\n".format("账户名","卡号","余额(RMB)"))
    print("|{0:<5}|{1:<20}|{2:<11}|\n".format(user_list[user_id]["name"],user_list[user_id]["numbers"],user_list[user_id]["balance"]))

#定义用户取款的函数
def withdrawal(amount):
    '''
    用户取款的函数
    '''
    i = user_list[user_id]["balance"]-int(amount)
    if i>=0:
        user_list[user_id]["balance"]-=int(amount)
    else:
        print("账户余额不足\n")

#定义用户存款的函数
def deposit(amount):
    '''
    用户存款的函数
    '''
    user_list[user_id]["balance"]+=int(amount)

#定义用户修改密码的函数
def change_password(old_password,new_password1,new_password2):
    '''
    用户修改密码的函数
    '''
    if old_password == user_list[user_id]["password"]:
        if new_password1 == new_password2:
            user_list[user_id]["password"] = new_password1
            print("新密码修改成功\n")
            return 1
        else:
            print("修改密码失败，您2次输入的新密码不一致\n")
            return 2
    else:
        print("旧密码输入错误\n")
        return 0


#用户登录界面，输入银行卡号和密码
chance = 3 #允许3次用户名或密码输入错误
while True:
    ATM()
    user_name = input("请输入您的银行卡卡号：")
    print("")
    print("请输入您的银行卡密码:", end=' ', flush=True)
    user_password = b''.join(psw_input()).decode()
    print("")

    user_id = check(user_name,user_password)#验证银行卡号与密码是否匹配

    if user_id != None:
        print("登录成功\n")

        while True:
            interface()
            key_word = input("请输入操作选项：")
            print("")
            if key_word == "1":
                inquire(user_id)
                input("按任意键返回上一级目录:")
                print("")
            elif key_word == "2":
                print("="*14,"账号取款界面","="*14,"\n")
                amount = input("请输入取款金额：")
                print("")
                withdrawal(amount)
                inquire(user_id)
                input("按任意键返回上一级目录:")
                print("")
            elif key_word == "3":
                print("="*14,"账号存款界面","="*14,"\n")
                amount = input("请输入存款金额：")
                print("")
                deposit(amount)
                inquire(user_id)
                input("按任意键返回上一级目录:")
                print("")
            elif key_word == "4":
                print("="*14,"密码管理界面","="*14,"\n")

                print("请输入旧密码:", end=' ', flush=True)
                old_password = b''.join(psw_input()).decode()
                print("")
                print("请输入新密码:", end=' ', flush=True)
                new_password1 = b''.join(psw_input()).decode()
                print("")
                print("请再次输入新密码:", end=' ', flush=True)
                new_password2 = b''.join(psw_input()).decode()
                print("")
                save = change_password(old_password,new_password1,new_password2)
                #如何检测到旧密码输入有误，将直接退出
                if save == 0:
                    break
            elif key_word == "5":
                print("="*14,"欢迎下次光临","="*14,"\n")
                break
            else:
                print("="*14,"没有该选项","="*14,"\n")
    else:
        if chance > 1:
            print("用户名或密码错误，您还有",chance-1,"次机会，请重新输入\n")
            chance -= 1
        else:
            print("对不起，您输入用户名或密码错误已达3次")
            break