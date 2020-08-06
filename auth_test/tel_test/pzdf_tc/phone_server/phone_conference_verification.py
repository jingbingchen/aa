import time
import traceback
import uuid

from pzdf_base_test_case import PzdfBaseTestCase
from pzdf_tc.phone_server import A8698Element
from tools.phone_utils import phoneUtils
import datetime
from random import choice


class PhoneConferenceCase(PzdfBaseTestCase):

    @classmethod
    def setUpClass(cls):
        cls.dial_ip = cls.param.get("dial_ip")
        cls.answer_ip = cls.param.get("answer_ip")
        cls.tripartite_ip = cls.param.get("tripartite_ip")
        cls.tripartite_two_ip = cls.param.get("tripartite_two_ip")
        cls.dial = cls.custom_device(cls, cls.dial_ip)
        cls.answer = cls.custom_device(cls, cls.answer_ip)
        cls.tripartite = cls.custom_device(cls, cls.tripartite_ip)
        cls.tripartite_two = cls.custom_device(cls, cls.tripartite_two_ip)

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
            print("当前错误：\n%s: %s\n     %s" % (typ, self.id(), msg))

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
        # 关闭电话服务
        phoneUtils.stop_app(self.dial, A8698Element.phone_service_package)
        phoneUtils.stop_app(self.answer, A8698Element.phone_service_package)
        phoneUtils.stop_app(self.tripartite, A8698Element.phone_service_package)
        phoneUtils.stop_app(self.tripartite_two, A8698Element.phone_service_package)
        # 解决出现多少个未接电话导致话机操作不了的问题
        self.dial.app_start(A8698Element.call_record_package)
        time.sleep(3)
        phoneUtils.stop_app(self.dial, A8698Element.call_record_package)
        # 启动App
        phoneUtils.reboot_app(self.dial, A8698Element.phone_conference_package)
        phoneUtils.stop_app(self.answer, A8698Element.phone_conference_package)
        phoneUtils.stop_app(self.tripartite, A8698Element.phone_conference_package)
        phoneUtils.stop_app(self.tripartite_two, A8698Element.phone_conference_package)

    def test_01(self):
        try:
            # 判断是否存在查看元素
            if self.dial(resourceId="com.android.pzPhone:id/btn_dialog_missedcall_check").exists(3):
                print("--> 初始化存在查看按钮先点击查看 【{}】".format(self.param.get("dial_ip")))
                self.dial.xpath('//*[@resource-id="com.android.pzPhone:id/btn_dialog_missedcall_check"]').click()
            # 点击关闭会议窗口
            if self.dial(resourceId="com.android.pzPhone:id/btn_testmedia_layout_exitscreen").exists(3):
                print("--> 初始化在视频会议页面 【{}】".format(self.param.get("dial_ip")))
                self.dial.xpath('//*[@resource-id="com.android.pzPhone:id/btn_testmedia_layout_exitscreen"]').click()
            # 点击关闭当前会议
            if self.dial(resourceId="com.pzdf.pzipteleconference:id/ibtn_conference_finish").exists(3):
                print("--> 初始化在会议进行中的页面 【{}】".format(self.param.get("dial_ip")))
                # 点击结束会议
                self.dial.xpath('//*[@resource-id="com.pzdf.pzipteleconference:id/ibtn_conference_finish"]').click()
                # 点击确定
                self.dial.xpath('//*[@resource-id="com.pzdf.pzipteleconference:id/btn_dialog_hint_confirm"]').click()
            # 判断是否在添加参会的人员的页面中 如果在就点击返回
            if self.dial(resourceId="com.pzdf.pzipteleconference:id/tvPersonnel").exists(3):
                print("--> 初始化启动存在在添加参会页面中 【{}】".format(self.param.get("dial_ip")))
                self.dial.xpath('//*[@resource-id="com.pzdf.pzipteleconference:id/btnBack"]').click()
            # 判断如果在参会页面
            if self.dial(resourceId="com.pzdf.pzipteleconference:id/tv_confirm_personnel").exists(3):
                print("--> 初始化启动在确认人员页面中 【{}】".format(self.param.get("dial_ip")))
                self.dial.xpath('//*[@resource-id="com.pzdf.pzipteleconference:id/btnBack"]').click()
            # 点击创建新会议
            self.dial.xpath('//*[@resource-id="com.pzdf.pzipteleconference:id/ibtnCreatMeet"]').click()
            time.sleep(1)
            # print(self.dial.xpath('//*[@text="输入号码"]').exists)
            self.assertTrue(self.dial.xpath('//*[@text="输入号码"]').exists)
            # 输入账号
            self.dial.xpath('//*[@text="输入号码"]').click()
            self.dial.xpath('//*[@resource-id="com.pzdf.pzipteleconference:id/editInputNumber"]').click()
            answer_code = self.param.get("code")
            self.dial.send_keys(answer_code, clear=True)
            input_phone = self.dial.xpath(
                '//*[@resource-id="com.pzdf.pzipteleconference:id/editInputNumber"]').get().attrib.get("text")
            print(input_phone)
            # 点击选择输入的话机
            self.dial.xpath('//*[@resource-id="com.pzdf.pzipteleconference:id/tvShowNumber"]').click()
            # 继续添加
            self.dial.xpath('//*[@resource-id="com.pzdf.pzipteleconference:id/editInputNumber"]').click()
            tripartite_code = self.param.get("tripartite_code")
            print(tripartite_code)
            self.dial.send_keys(tripartite_code, clear=True)
            input_phone = self.dial.xpath(
                '//*[@resource-id="com.pzdf.pzipteleconference:id/editInputNumber"]').get().attrib.get("text")
            print(input_phone)
            self.dial.xpath('//*[@resource-id="com.pzdf.pzipteleconference:id/tvShowNumber"]').click()
            # 继续添加
            self.dial.xpath('//*[@resource-id="com.pzdf.pzipteleconference:id/editInputNumber"]').click()
            tripartite_two_code = self.param.get("tripartite_two_code")
            print(tripartite_two_code)
            self.dial.send_keys(tripartite_two_code, clear=True)
            input_phone = self.dial.xpath(
                '//*[@resource-id="com.pzdf.pzipteleconference:id/editInputNumber"]').get().attrib.get("text")
            print(input_phone)
            self.dial.xpath('//*[@resource-id="com.pzdf.pzipteleconference:id/tvShowNumber"]').click()
            pass
        except Exception as e:
            print("--> 当前错误元素 IP:【{}】 code: 【{}】".format(self.param.get("dial_ip"), self.param.get("dial_code")))
            traceback.print_exc()

    def test_02(self):
        # 点击进入会场
        self.dial.xpath('//*[@resource-id="com.pzdf.pzipteleconference:id/ibEnterRoom"]').click()
        # 点击视频会议
        self.dial.xpath('//*[@resource-id="com.pzdf.pzipteleconference:id/btn_convene_conference"]').click()

    def test_03(self):
        try:
            # 点击接听
            self.answer.xpath('//*[@text="视频接听"]').click()
            self.tripartite.xpath('//*[@text="视频接听"]').click()
            self.tripartite_two.xpath('//*[@text="视频接听"]').click()
        except Exception as e:
            print("--> answer当前错误元素 IP:【{}】  code: 【{}】".format(self.param.get("answer_ip"), self.param.get("code")))
            print("--> tripartite当前错误元素 IP:【{}】  code: 【{}】".format(self.param.get("tripartite_ip"),
                                                                    self.param.get("tripartite_code")))
            print("--> tripartite_two当前错误元素 IP:【{}】 code: 【{}】".format(self.param.get("tripartite_two_ip"),
                                                                       self.param.get("tripartite_two_code")))
            traceback.print_exc()

        foos = [0, 1, 2]
        operatings = [0, 1, 2]
        # 开始循环操作
        endTime = datetime.datetime.now() + datetime.timedelta(minutes=30)
        print(endTime)

        def execution_operating(d, operating):
            if operating == 0:
                d.click(164, 265)
                time.sleep(2)
                if d.xpath('//*[@resource-id="com.android.pzPhone:id/btn_activity_video_call_screencap"]').exists:
                    # 点击隐藏小窗口
                    d.xpath('//*[@resource-id="com.android.pzPhone:id/btn_activity_video_call_screencap"]').click()

            elif operating == 1:
                d.click(164, 265)
                time.sleep(2)
                if d.xpath('//*[@resource-id="com.android.pzPhone:id/btn_activity_video_call_caver"]').exists:
                    # 点击隐藏小窗口
                    d.xpath('//*[@resource-id="com.android.pzPhone:id/btn_activity_video_call_caver"]').click()

            elif operating == 2:
                d.click(164, 265)
                time.sleep(2)
                if d.xpath('//*[@resource-id="com.android.pzPhone:id/btn_activity_video_call_updatesize"]').exists:
                    d.xpath('//*[@resource-id="com.android.pzPhone:id/btn_activity_video_call_updatesize"]').click()

        while True:
            if datetime.datetime.now() >= endTime:
                print(datetime.datetime.now())
                break
            else:
                foo = choice(foos)
                if foo == 0:
                    operating = choice(operatings)
                    execution_operating(self.answer, operating)
                elif foo == 1:
                    operating = choice(operatings)
                    execution_operating(self.tripartite, operating)
                elif foo == 2:
                    operating = choice(operatings)
                    execution_operating(self.tripartite_two, operating)

    def test_04(self):
        # 退出全屏
        self.dial.xpath('//*[@resource-id="com.android.pzPhone:id/btn_testmedia_layout_exitscreen"]').click()
        # 点击结束会议
        self.dial.xpath('//*[@resource-id="com.pzdf.pzipteleconference:id/ibtn_conference_finish"]').click()
        # 判断提示语
        dial_hint = self.dial.xpath(
            '//*[@resource-id="com.pzdf.pzipteleconference:id/tv_dialog_hint_message"]').get().attrib.get("text")
        # 点击确定
        self.dial.xpath('//*[@resource-id="com.pzdf.pzipteleconference:id/btn_dialog_hint_confirm"]').click()
