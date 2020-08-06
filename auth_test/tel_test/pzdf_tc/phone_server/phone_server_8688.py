import time

from base_logging import log
from pzdf_base_test_case import PzdfBaseTestCase
from tools.phone_utils import phoneUtils


# 保持/恢复
class PhoneServerCallHoldTestCase(PzdfBaseTestCase):

    @classmethod
    def setUpClass(cls):
        dial_ip = cls.param.get("dial_ip")
        answer_ip = cls.param.get("answer_ip")
        log.info("终端[{}]测试开始", cls.param)
        log.info("拨号终端[{}]初始化状态", dial_ip)
        log.info("接听终端[{}]初始化状态", answer_ip)

        cls.dial = cls.custom_device(cls, dial_ip)
        cls.answer = cls.custom_device(cls, answer_ip)
        # 初始化主叫
        pid = cls.dial.app_wait("com.android.pzPhone", front=True, timeout=1.0)
        if not pid:
            log.info("终端[{}]测试APP[{}]启动", dial_ip, "com.android.pzPhone")
            cls.dial.app_start("com.android.pzPhone")
        else:
            log.info("终端[{}]测试APP[{}，{}]关闭，重启", dial_ip, "com.android.pzPhone", pid)
            phoneUtils.stop_app(cls.dial, "com.android.pzPhone")
            cls.dial.app_start("com.android.pzPhone")
        # 初始化被叫
        pid = cls.answer.app_wait("com.android.pzPhone", front=True, timeout=1.0)
        if not pid:
            log.info("终端[{}]测试APP[{}]关闭状态", answer_ip, "com.android.pzPhone")
        else:
            log.info("终端[{}]测试APP[{}，{}]关闭", answer_ip, "com.android.pzPhone", pid)
            phoneUtils.stop_app(cls.answer, "com.android.pzPhone")

    @classmethod
    def tearDownClass(cls):
        log.info("终端[{}]测试结束", cls.param)
        is_hole = cls.dial(resourceId="com.android.pzPhone:id/btn_phone_activity_hangup").exists()
        if is_hole:
            log.error("终端[{}]，通话异常未挂断，挂断电话", cls.param.get("dial_ip"))
            cls.dial(resourceId="com.android.pzPhone:id/btn_phone_activity_hangup").click()

    def test_000_phone(self):
        """
        主叫拨号
        """
        log.info("[{}]话机拨号：[{}]", self.param.get("dial_ip"), self.param.get("code"))
        phoneUtils.phone_dial(self.dial, self.param.get("code"))

    def test_100_call_answer(self):
        log.info("[{}]话机接听", self.param.get("answer_ip"))
        phoneUtils.phone_answer(self.answer)

    def test_200_call_hold(self):
        """
        电话保持/恢复
        """
        # 等待接听 20 秒
        self.dial.implicitly_wait(20.0)
        self.dial(resourceId="com.android.pzPhone:id/btn_phone_activity_hold").exists()
        time.sleep(5)
        # 保持
        self.dial(resourceId="com.android.pzPhone:id/btn_one_button_item", text="保持").click()
        state = self.dial(resourceId="com.android.pzPhone:id/tv_activity_phone_main_state").get_text()
        self.assertEqual(state, "保持中", "主叫保持失败")
        time.sleep(1)
        state = self.answer(resourceId="com.android.pzPhone:id/tv_activity_phone_main_state").get_text()
        self.assertEqual(state, "被保持", "被叫保持失败")
        time.sleep(5)

    def test_201_call_hold_state(self):
        # 恢复
        self.dial(resourceId="com.android.pzPhone:id/btn_one_button_item", text="恢复").click()
        state = self.dial(resourceId="com.android.pzPhone:id/tv_activity_phone_main_state").get_text()
        self.assertEqual(state, "通话中", "主叫恢复失败")
        time.sleep(1)
        state = self.answer(resourceId="com.android.pzPhone:id/tv_activity_phone_main_state").get_text()
        self.assertEqual(state, "通话中", "被叫恢复失败")
        time.sleep(5)

    def test_202_call_hangup(self):
        # 电话挂机
        phoneUtils.phone_hangup(self.dial)


# 三方新通话
class PhoneServerTripartiteTestCase(PzdfBaseTestCase):

    @classmethod
    def setUpClass(cls):
        dial_ip = cls.param.get("dial_ip")
        answer_ip = cls.param.get("answer_ip")
        tripartite_ip = cls.param.get("tripartite_ip")
        log.info("终端[{}]测试开始", cls.param)
        log.info("拨号终端[{}]初始化状态", dial_ip)
        log.info("接听终端[{}]初始化状态", answer_ip)
        log.info("三方终端[{}]初始化状态", tripartite_ip)

        cls.dial = cls.custom_device(cls, dial_ip)
        cls.answer = cls.custom_device(cls, answer_ip)
        cls.tripartite = cls.custom_device(cls, tripartite_ip)
        pid = cls.dial.app_wait("com.android.pzPhone", front=True, timeout=1.0)  # 等待应用运行, return pid(int)
        if not pid:
            log.info("终端[{}]测试APP[{}]启动", dial_ip, "com.android.pzPhone")
            cls.dial.app_start("com.android.pzPhone")
        else:
            log.info("终端[{}]测试APP[{}，{}]关闭，重启", dial_ip, "com.android.pzPhone", pid)
            phoneUtils.stop_app(cls.dial, "com.android.pzPhone")
            cls.dial.app_start("com.android.pzPhone")
        # 初始化被叫
        pid = cls.answer.app_wait("com.android.pzPhone", front=True, timeout=1.0)
        if not pid:
            log.info("终端[{}]测试APP[{}]关闭状态", answer_ip, "com.android.pzPhone")
        else:
            log.info("终端[{}]测试APP[{}，{}]关闭", answer_ip, "com.android.pzPhone", pid)
            phoneUtils.stop_app(cls.answer, "com.android.pzPhone")
        # 初始化第三方通过
        pid = cls.tripartite.app_wait("com.android.pzPhone", front=True, timeout=1.0)
        if not pid:
            log.info("终端[{}]测试APP[{}]关闭状态", tripartite_ip, "com.android.pzPhone")
        else:
            log.info("终端[{}]测试APP[{}，{}]关闭", tripartite_ip, "com.android.pzPhone", pid)
            phoneUtils.stop_app(cls.tripartite, "com.android.pzPhone")

    @classmethod
    def tearDownClass(cls):
        log.info("终端[{}]测试结束", cls.param)
        is_hole = cls.dial(resourceId="com.android.pzPhone:id/btn_phone_activity_hangup").exists()
        if is_hole:
            log.error("终端[{}]，通话异常未挂断，挂断电话", cls.param.get("dial_ip"))
            cls.dial(resourceId="com.android.pzPhone:id/btn_phone_activity_hangup").click()

    def test_000_phone(self):
        """
        主叫拨号
        """
        log.info("[{}]话机拨号：[{}]", self.param.get("dial_ip"), self.param.get("code"))
        phoneUtils.phone_dial(self.dial, self.param.get("code"))

    def test_100_call_answer(self):
        log.info("[{}]话机接听", self.param.get("answer_ip"))
        phoneUtils.phone_answer(self.answer)

    def test_200_call_transfer(self):
        tripartite_code = self.param.get("tripartite_code")
        log.info("[{}]话机，新呼叫至[{}]话机[{}]号码",
                 self.param.get("answer_ip"), self.param.get("tripartite_ip"), tripartite_code)
        # 等待新呼叫 20 秒
        self.answer.implicitly_wait(20.0)
        item_len = len(self.answer(resourceId="com.android.pzPhone:id/btn_one_button_item"))
        self.assertEqual(item_len, 6, "按钮数量不正确")
        # 新通话
        self.answer(resourceId="com.android.pzPhone:id/btn_one_button_item")[4].click()
        time.sleep(1)
        log.info("[{}]话机拨[{}]号码",
                 self.param.get("answer_ip"), tripartite_code)
        phoneUtils.click_numeral(self.answer, tripartite_code)
        phone_code = self.answer.xpath('//android.widget.EditText[1]').get().attrib.get("text")
        self.assertEqual(phone_code, tripartite_code, "号码输入错误")
        time.sleep(.5)
        # 语音拨号
        self.answer(resourceId="com.android.pzPhone:id/activity_rightbutton_lager").click()

    def test_300_call_answer(self):
        log.info("[{}]话机接听", self.param.get("tripartite_ip"))
        # 第三方话机接听
        phoneUtils.phone_answer(self.tripartite)
        state = self.tripartite(resourceId="com.android.pzPhone:id/tv_activity_phone_main_state").get_text()
        self.assertEqual(state, "通话中", "接听失败")
        time.sleep(1)

    def test_400_call_hold_tripartite(self):
        time.sleep(5)
        # 电话挂机
        phoneUtils.phone_hangup(self.answer)

    def test_500_call_restore_dial(self):
        # 恢复第一方
        self.answer(resourceId="com.android.pzPhone:id/btn_one_button_item")[2].click()
        time.sleep(.5)
        state = self.answer(resourceId="com.android.pzPhone:id/tv_activity_phone_main_state").get_text()
        self.assertEqual(state, "通话中", "恢复失败")
        state = self.answer(resourceId="com.android.pzPhone:id/btn_one_button_item")[2].get_text()
        self.assertEqual(state, "保持", "恢复失败，按钮还是恢复按钮")

    def test_600_call_hold_dial(self):
        time.sleep(5)
        # 电话挂机
        phoneUtils.phone_hangup(self.answer)