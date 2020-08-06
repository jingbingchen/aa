import time

from pzdf_base_test_case import PzdfBaseTestCase
from pzdf_tc.phone_server import A8698Element
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
        phoneUtils.reboot_app(self.dial, A8698Element.phone_service_package)
        phoneUtils.stop_app(self.answer, A8698Element.phone_service_package)
        phoneUtils.stop_app(self.tripartite, A8698Element.phone_service_package)

    def test_01(self):
        # 输入号码
        phoneUtils.click_numeral_button(self.dial, self.param.get("code"))
        phone_code = self.dial.xpath('//android.widget.EditText[1]').get().attrib.get("text")
        self.assertEqual(self.param.get("code"), phone_code)

    def test_02(self):
        # 点击视频通话
        self.dial.xpath('//*[@text="视频通话"]').click()
        # 获得头部标题
        dial_phone_state = self.dial.xpath(
            '//*[@resource-id="com.android.pzPhone:id/tv_activity_phone_main_state2"]').get().attrib.get("text")
        print(dial_phone_state)
        # 判断是否 == 拨号中
        self.assertEqual("拨号中", dial_phone_state)
        answer_phone_state = self.answer.xpath(
            '//*[@resource-id="com.android.pzPhone:id/tv_activity_phone_main_state2"]').get().attrib.get("text")
        print(answer_phone_state)
        self.assertEqual("来电中", answer_phone_state)

    def test_03(self):
        # 接听
        self.answer.xpath('//*[@text="视频接听"]').click()
        time.sleep(1)
        # 判断是否都在通话中状态
        dial_phone_state = self.dial(resourceId=A8698Element.video_call_name).get_text()
        print(dial_phone_state)
        self.assertEqual(self.param.get("dial_code"), dial_phone_state)
        answer_phone_state = self.answer(resourceId=A8698Element.video_call_name).get_text()
        print(answer_phone_state)
        self.assertEqual(self.param.get("code"), answer_phone_state)

    def test_04(self):
        # 点击屏幕一下出现隐藏域
        self.dial.click(164, 265)
        # 点击隐藏小窗口
        self.dial.xpath('//*[@resource-id="com.android.pzPhone:id/btn_activity_video_call_caver"]').click()
        # 判断是否已经隐藏
        self.assertFalse(
            self.dial.xpath('//*[@resource-id="com.android.pzPhone:id/cv_activity_viedo_call_small"]').exists)
        # 点击退出全屏
        self.dial.xpath('//*[@resource-id="com.android.pzPhone:id/btn_activity_video_call_exitscreen"]').click()
        # 判断是否已经退出
        self.assertTrue(self.dial.xpath('//*[@text="语音通话"]').exists)

    def test_05(self):
        self.dial.xpath('//*[@text="转接"]').click()
        phoneUtils.click_numeral(self.dial, self.param.get("tripartite_code"))
        # 视频拨打电话
        self.dial.xpath('//*[@text="视频通话"]').click()
        # 点击视频接听
        self.tripartite.xpath('//*[@text="视频接听"]').click()
        # 点击挂断
        self.dial.click(164, 265)
        self.dial.xpath('//*[@resource-id="com.android.pzPhone:id/btn_activity_video_call_hangup"]').click()

        # dial_phone_state = self.dial(resourceId=A8698Element.video_call_name).get_text()
        # print(dial_phone_state)
        # 点击恢复
        self.dial.xpath('//*[@text="恢复"]').click()
        #
        # dial_phone_state = self.dial(resourceId=A8698Element.video_call_name).get_text()
        # print(dial_phone_state)
        # self.assertEqual(self.param.get("dial_code"), dial_phone_state)
        # 点击挂断
        self.dial.click(164, 265)
        self.dial.xpath('//*[@resource-id="com.android.pzPhone:id/btn_activity_video_call_hangup"]').click()

        time.sleep(2)
        dial_pid = self.dial.app_wait(A8698Element.phone_service_package, front=True, timeout=1.0)
        answer_pid = self.answer.app_wait(A8698Element.phone_service_package, front=True, timeout=1.0)
        # 判断是否都返回的首页了
        self.assertTrue(dial_pid == 0)
        self.assertTrue(answer_pid == 0)
