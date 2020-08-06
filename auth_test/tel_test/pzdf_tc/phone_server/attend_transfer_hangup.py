import time

from pzdf_base_test_case import PzdfBaseTestCase
from pzdf_tc.phone_server import A8668Element
from tools.phone_utils import phoneUtils


class TestCase(PzdfBaseTestCase):

    @classmethod
    def setUpClass(cls):
        cls.dial_ip = cls.param.get("dial_ip")
        cls.answer_ip = cls.param.get("answer_ip")
        cls.tripartite_ip = cls.param.get("tripartite_ip")
        cls.dial = cls.custom_device(cls, cls.dial_ip)
        cls.answer = cls.custom_device(cls, cls.answer_ip)
        cls.tripartite = cls.custom_device(cls, cls.tripartite_ip)

    def test_00(self):
        # 启动App
        phoneUtils.reboot_app(self.dial, A8668Element.phone_service_package)
        phoneUtils.stop_app(self.answer, A8668Element.phone_service_package)
        phoneUtils.stop_app(self.tripartite, A8668Element.phone_service_package)

    def test_01(self):
        # 输入号码
        phoneUtils.click_numeral_button(self.dial, self.param.get("code"))
        phone_code = self.dial.xpath('//android.widget.EditText[1]').get().attrib.get("text")
        self.assertEqual(self.param.get("code"), phone_code)

    def test_02(self):
        # 点击语音通话
        self.dial(resourceId=A8668Element.voice_calls_button).click()
        # 获得头部标题
        dial_phone_state = self.dial(resourceId=A8668Element.phone_main_state).get_text()
        # 判断是否 == 拨号中
        self.assertEqual("拨号中", dial_phone_state)
        answer_phone_state = self.answer(resourceId=A8668Element.phone_main_state).get_text()
        self.assertEqual("来电中", answer_phone_state)

    def test_03(self):
        # 接听
        self.answer(resourceId=A8668Element.answer_button).click()
        time.sleep(1)
        # 判断是否都在通话中状态
        dial_phone_state = self.dial(resourceId=A8668Element.phone_main_state).get_text()
        self.assertEqual("通话中", dial_phone_state)
        answer_phone_state = self.answer(resourceId=A8668Element.phone_main_state).get_text()
        self.assertEqual("通话中", answer_phone_state)

    def test_04(self):
        # 点击转接
        self.answer(text=A8668Element.forward_button).click()
        dial_phone_state = self.dial(resourceId=A8668Element.phone_main_state).get_text()
        self.assertEqual("被保持", dial_phone_state)
        answer_pid = self.answer.app_wait(A8668Element.phone_service_package, front=True, timeout=1.0)
        # 判断是否回到主页
        self.assertTrue(answer_pid == 0)

    def test_05(self):
        phoneUtils.click_numeral(self.answer, self.param.get("tripartite_code"))
        # 拨号完点击语音拨打电话
        self.answer(resourceId=A8668Element.voice_calls_button).click()
        time.sleep(2)
        # 判断当前头部显示是否是两个号码
        self.assertTrue(len(self.answer(resourceId=A8668Element.phone_radio_name)) == 2)
        self.assertEqual(self.param.get("dial_code"),
                         self.answer(resourceId=A8668Element.phone_radio_name)[0].get_text())
        self.assertEqual(self.param.get("tripartite_code"),
                         self.answer(resourceId=A8668Element.phone_radio_name)[1].get_text())
        dial_phone_state = self.dial(resourceId=A8668Element.phone_main_state).get_text()
        self.assertEqual("被保持", dial_phone_state)
        # 判断转接号码标题是否正确
        tripartite_phone_state = self.tripartite(resourceId=A8668Element.phone_main_state).get_text()
        self.assertEqual("来电中", tripartite_phone_state)

    def test_06(self):
        self.tripartite(text=A8668Element.hang_up_button).click()
        dial_phone_state = self.dial(resourceId=A8668Element.phone_main_state).get_text()
        self.assertEqual("被保持", dial_phone_state)
        tripartite_pid = self.tripartite.app_wait(A8668Element.phone_service_package, front=True, timeout=1.0)
        self.assertTrue(tripartite_pid == 0)
        # 您有1个未接来电”提示框
        if self.answer(resourceId=A8668Element.phone_main_state).exists(60):
            dial_phone_state = self.answer(resourceId=A8668Element.phone_main_state).get_text()
            self.assertEqual("保持中", dial_phone_state)

    def test_07(self):
        # 点击挂断
        self.dial(text=A8668Element.hang_up_button).click()
        time.sleep(2)
        dial_pid = self.dial.app_wait(A8668Element.phone_service_package, front=True, timeout=1.0)
        answer_pid = self.answer.app_wait(A8668Element.phone_service_package, front=True, timeout=1.0)
        # 判断是否都返回的首页了
        self.assertTrue(dial_pid == 0)
        self.assertTrue(answer_pid == 0)
