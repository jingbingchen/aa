import uiautomator2 as u2

ip = "192.168.0.227"
ip2 = '192.168.0.164'

d = u2.connect_wifi(ip)
#d2 = u2.connect_wifi(ip2)
import time

num = "9226"


def test():
    for i in range(1, 100000):
        try:
            d.app_start("com.android.pzPhone")
            for a in str(num):
                d(resourceId="com.android.pzPhone:id/btn_phone_{}".format(a)).click()
            d(resourceId="com.android.pzPhone:id/activity_rightbutton_lager").click()
            #d2(resourceId="com.android.pzPhone:id/activity_rightbutton_lager").click()
            # d(resourceId="com.android.pzPhone:id/activity_rightbutton_lager", text="挂断").click()
            d.xpath('//*[@resource-id="com.android.pzPhone:id/activity_rightbutton_lager"]').click()
        except:
            print(i, "次出错")
        else:
            print("-----------")

    # d.app_start("com.pzdf.phoneconfiguration")
    # d.swipe(82, 434, 82, 112)
    # d(resourceId="com.pzdf.phoneconfiguration:id/textView_title", text="安全").click()


test()
