import time

from pzdf_base_test_case import PzdfBaseTestCase


class PhoneUtils(PzdfBaseTestCase):

    # 关闭APP 由于我们的话机调用原生的方法不起作用
    def stop_app(self, d, package_name):
        # 先获得当前应用PID
        pid = d.app_wait(package_name, front=False, timeout=1.0)
        if pid:
            # kill 当前程序进程
            d.shell("kill {0}".format(pid))

    def phone_dial(self, d, number, is_button=True):
        """
        拨号
        """
        title = d(resourceId="com.android.pzPhone:id/tv_dial_activity_title").get_text()
        self.assertEqual(title, "拨号", "拨号界面未启动")
        if is_button:
            self.click_numeral_button(d, number)
        else:
            self.click_numeral(d, number)
        phone_code = d.xpath('//android.widget.EditText[1]').get().attrib.get("text")
        self.assertEqual(phone_code, number, "号码输入错误")
        self.click_voice_button(d)
        state = d(resourceId="com.android.pzPhone:id/tv_activity_phone_main_state").get_text()
        self.assertEqual(state, "拨号中", "拨号失败")

    def phone_hangup(self, d):
        """
        挂断
        """
        # 挂断
        bangup_text = d(resourceId="com.android.pzPhone:id/activity_rightbutton_lager").get_text()
        self.assertEqual(bangup_text, "挂断", "挂断按钮不存在")
        d(resourceId="com.android.pzPhone:id/activity_rightbutton_lager").click()
        time.sleep(1)
        # 判断是否已经挂断(多方通话有问题)
        # is_hole = d(resourceId="com.android.pzPhone:id/activity_rightbutton_lager").exists()
        # self.assertFalse(is_hole, "挂断失败")

    def phone_answer(self, d):
        """
        接听
        """
        d.implicitly_wait(20.0)
        answer_text = d(resourceId="com.android.pzPhone:id/activity_rightbutton_lager").get_text()
        self.assertEqual(answer_text, "接听", "接听按钮不存在")
        d(resourceId="com.android.pzPhone:id/activity_rightbutton_lager").click()
        time.sleep(1)
        state = d(resourceId="com.android.pzPhone:id/tv_activity_phone_main_state").get_text()
        self.assertEqual(state, "通话中", "接听失败")

    # 点击数字按钮
    def click_numeral_button(self, d, phone):
        for numeral in phone:
            d(resourceId="com.android.pzPhone:id/btn_phone_{0}".format(numeral)).click()

    def click_voice_button(self, d, is_voice=True):
        # 点击语音通话
        if (is_voice):
            voice_text = d(resourceId="com.android.pzPhone:id/activity_rightbutton_lager").get_text()
            self.assertEqual(voice_text, "语音通话", "语音通话按钮不存在")
            d(resourceId="com.android.pzPhone:id/activity_rightbutton_lager").click()

    def click_numeral(self, d, phone):
        for numeral in phone:
            time.sleep(1)
            if numeral == '0':
                d.press(0x00000007, 0x00000002)
            elif numeral == '1':
                d.press(0x00000008, 0x00000002)
            elif numeral == '2':
                d.press(0x00000009, 0x00000002)
            elif numeral == '3':
                d.press(0x0000000A, 0x00000002)
            elif numeral == '4':
                d.press(0x0000000B, 0x00000002)
            elif numeral == '5':
                d.press(0x0000000C, 0x00000002)
            elif numeral == '6':
                d.press(0x0000000D, 0x00000002)
            elif numeral == '7':
                d.press(0x0000000E, 0x00000002)
            elif numeral == '8':
                d.press(0x0000000F, 0x00000002)
            elif numeral == '9':
                d.press(0x00000010, 0x00000002)

    def reboot_app(self, d, package_name):
        self.stop_app(d, package_name)
        d.app_start(package_name)


phoneUtils = PhoneUtils()
