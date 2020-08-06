import os
import time
import uuid
from pathlib import Path

# 盲转成功
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

    def list2reason(self, exc_list):
        if exc_list and exc_list[-1][0] is self:
            return exc_list[-1][1]

    def tearDown(self):
        uid = str(uuid.uuid4())
        suid = ''.join(uid.split('-'))
        if hasattr(self, '_outcome'):
            result = self.defaultTestResult()
            self._feedErrorsToResult(result, self._outcome.errors)
        error = self.list2reason(result.errors)
        failure = self.list2reason(result.failures)
        ok = not error and not failure
        if not ok:
            typ, text = ('ERROR', error) if error else ('FAIL', failure)
            msg = [x for x in text.split('\n')[1:] if not x.startswith(' ')][0]
            print("\n%s: %s\n     %s" % (typ, self.id(), msg))

            # def creat_file_path(file_path):
            #     dir_name = Path(file_path)
            #     # 判断当前文件目录是否存在 如果不存在就创建
            #     if not dir_name.exists():
            #         os.makedirs(dir_name)
            #
            # print(".| 当前错误图片目录 【./img/{}】".format(suid))
            #
            # dial_image = self.dial.screenshot()
            # creat_file_path("./img/{}".format(suid))
            # dial_image.save("./img/{}/{}.png".format(suid, self.dial.serial))  # 图片名字自定义
            #
            # answer_image = self.answer.screenshot()
            # answer_image.save("./img/{}/{}.png".format(suid, self.answer.serial))  # 图片名字自定义
            #
            # tripartite_image = self.tripartite.screenshot()
            # tripartite_image.save("./img/{}/{}.png".format(suid, self.tripartite.serial))  # 图片名字自定义

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
        # 点击语音通话
        self.dial(resourceId=A8698Element.voice_calls_button).click()
        # 获得头部标题
        dial_phone_state = self.dial(resourceId=A8698Element.phone_main_state).get_text()
        # 判断是否 == 拨号中
        self.assertEqual("拨号中", dial_phone_state)
        answer_phone_state = self.answer(resourceId=A8698Element.phone_main_state).get_text()
        self.assertEqual("来电中", answer_phone_state)

    def test_03(self):
        # 接听
        self.answer.xpath('//*[@resource-id="com.android.pzPhone:id/activity_rightbutton_lager"]').click()
        # # 判断是否都在通话中状态
        dial_phone_state = self.dial(resourceId=A8698Element.phone_main_state).get_text()
        self.assertEqual("通话中", dial_phone_state)
        answer_phone_state = self.answer(resourceId=A8698Element.phone_main_state).get_text()
        self.assertEqual("通话中", answer_phone_state)

    def test_04(self):
        # 点击转接
        self.answer.xpath('//*[@text="转接"]').click()
        dial_phone_state = self.dial(resourceId=A8698Element.phone_main_state).get_text()
        print(dial_phone_state)
        self.assertEqual("被保持", dial_phone_state)
        answer_pid = self.answer.app_wait(A8698Element.phone_service_package, front=True, timeout=1.0)
        # 判断是否回到主页
        self.assertTrue(answer_pid == 0)

    def test_05(self):
        phoneUtils.click_numeral(self.answer, self.param.get("tripartite_code"))
        phone_code = self.answer.xpath('//android.widget.EditText[1]').get().attrib.get("text")
        self.assertEqual(phone_code, self.param.get("tripartite_code"))
        # 拨号完点击语音拨打电话
        # self.answer(text=A8698Element.forward_button).click()
        self.answer(resourceId="com.android.pzPhone:id/btn_one_button_item", text="转接").click()
        # self.answer.xpath('//*[@text="转接"]').click()
        time.sleep(2)
        # 判断转接号码标题是否正确
        # answer_phone_state = self.answer(resourceId=A8698Element.phone_main_state).get_text()
        # self.assertEqual("正在转接中", answer_phone_state)
        dial_phone_state = self.dial(resourceId=A8698Element.phone_main_state).get_text()
        self.assertEqual("通话中", dial_phone_state)
        tripartite_phone_state = self.tripartite(resourceId=A8698Element.phone_main_state).get_text()
        self.assertEqual("来电中", tripartite_phone_state)

    def test_06(self):
        # 收到转接来的话机点击接听
        self.tripartite.xpath('//*[@resource-id="com.android.pzPhone:id/activity_rightbutton_lager"]').click()
        time.sleep(2)
        # 转接出去的话机挂断
        answer_pid = self.answer.app_wait(A8698Element.phone_service_package, front=True, timeout=1.0)
        self.assertTrue(answer_pid == 0)
        # 打电话的话机是通话中
        dial_phone_state = self.dial(resourceId=A8698Element.phone_main_state).get_text()
        self.assertEqual("通话中", dial_phone_state)
        # 收到转接来的话机也是通话中
        dial_phone_state = self.tripartite(resourceId=A8698Element.phone_main_state).get_text()
        self.assertEqual("通话中", dial_phone_state)

    def test_07(self):
        # 点击挂断
        # self.dial(text=A8698Element.hang_up_button).click()
        self.dial.xpath('//*[@text="挂断"]').click()
        time.sleep(2)
        dial_pid = self.dial.app_wait(A8698Element.phone_service_package, front=True, timeout=1.0)
        tripartite_pid = self.tripartite.app_wait(A8698Element.phone_service_package, front=True, timeout=1.0)
        # 判断是否都返回的首页了
        self.assertTrue(dial_pid == 0)
        self.assertTrue(tripartite_pid == 0)
