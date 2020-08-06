   # def fool(x):
#     return x+3
# a=fool(3)
# a=fool(4)+56
# print(fool(3))



goods_list = [{"name":"蔬菜","cost":100,}]




def print_info():
    print("********周记账簿小程序********")
    print("1.查询一周支出物品及其价格")
    print("2.添加所花费的物品及其价格")
    print("3.删除所花费的物品及其价格")
    print("4.修改所花费的物品及其价格")
    print("5.退出系统")
    user_input = input(">>>请输入您要操作的序号:")
    return user_input

def show_all_list_info():
    for goods in goods_list:
        print(goods)

def search_goods_info():
    user_input_name = input("请输入带搜索的商品名称：")
    goods_exist = False
    for goods in goods_list:
        if goods["name"] == user_input_name:
            goods_exist = True
            print(goods)
        if goods_exist != True:
            print("您要搜索的物品不存在")

def add_goods_info():
    # for i in range(7):
    name = input("请输入要添加的商品名称")
    cost = input("请输入添加的商品的价格")
    new_list = {"name":name,"cost":cost}
    goods_list.append(new_list)
    print("您添加的商品{}成功添加".format(name))
def del_goods_info():
    name = input("请输入要删除的商品名称")
    goods_exist = False
    for goods  in goods_list:
        if goods ['name'] == name:
            goods_exist =  True
            goods_list.remove(goods)
            print("您要删除的商品{}成功删除",format(name))
    if not goods_exist:
        print("您要删除的商品{}不存在",format(name))

def modify_goods_info():
    name = input("请输入要修改的商品名称")
    goods_exist = False
    for goods in goods_list:
        if goods['name'] == name:
            goods_exist = True
            new_goods = input("请输入修改后的商品名称")
            new_goods_cost =input("请输入修改后的价格")
            goods['name'] = new_goods
            goods['cost'] = new_goods_cost
            print("您要修改的商品{}修改成功",format(name))
    if not goods_exist:
        print("您要修改的商品{}不存在",format())




def run():
    while True:
        user_input = print_info()
        if user_input not in ["1","2","3","4","5"]:
            print("输入有误，请重新输入")
        else:
            if user_input == "1":
                show_all_list_info()
            elif user_input == "2":
                add_goods_info()
            elif user_input == "3":
                del_goods_info()
            elif user_input == "4":
                modify_goods_info()
            elif user_input == "5":
                print("欢迎下次再来")
                break
run()