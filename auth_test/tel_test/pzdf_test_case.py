import traceback

from BeautifulReport import BeautifulReport

from pzdf_tc.phone_server.phone_conference_six_verification import PhoneConferenceSixCase
from pzdf_tc.phone_server.phone_conference_verification import PhoneConferenceCase
from pzdf_tc.phone_server.phone_server_8688 import PhoneServerCallHoldTestCase, PhoneServerTripartiteTestCase
import unittest

from pzdf_tc.phone_server.video_function_check import TestCase
from tools.my_beautiful_report import MyBeautifulReport


def call_hold_test_case(param):
    testloader = unittest.TestLoader()
    testnames = testloader.getTestCaseNames(PhoneServerCallHoldTestCase)
    suite = unittest.TestSuite()
    for name in testnames:
        suite.addTest(
            PhoneServerCallHoldTestCase(name, param=param))
    unittest.TextTestRunner(verbosity=2).run(suite)


def tripartite_test_case(param):
    testloader = unittest.TestLoader()
    testnames = testloader.getTestCaseNames(PhoneServerTripartiteTestCase)
    suite = unittest.TestSuite()
    for name in testnames:
        suite.addTest(
            PhoneServerTripartiteTestCase(name, param=param))
    unittest.TextTestRunner(verbosity=2).run(suite)


def blind_turn_answer_case(param):
    testloader = unittest.TestLoader()
    testnames = testloader.getTestCaseNames(TestCase)
    suite = unittest.TestSuite()
    for name in testnames:
        suite.addTest(
            TestCase(name, param=param))
    unittest.TextTestRunner(verbosity=2).run(suite)


def blind_turn_answer_case_result(param):
    suite = unittest.TestSuite()
    testloader = unittest.TestLoader()
    testnames = testloader.getTestCaseNames(TestCase)
    for i in range(param["cycle_number"]):
        for name in testnames:
            suite.addTest(
                TestCase(name, param=param))
        # suite.addTest(PzdfBaseTestCase.parametrize(TestCase, param=param))
    result = BeautifulReport(suite)
    result.report(filename=param["dial_ip"], description='测试deafult报告', report_dir='report')
    # unittest.TextTestRunner(verbosity=2).run(suite)


def attend_transfer_verification(param):
    try:
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(TestCase)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(
                TestCase(name, param=param))
        result = MyBeautifulReport(suite)
        result.run_result_report()
        # for test_info in result.fields["testResult"]:
        #     # print(test_info["log"])
        #     uid = str(uuid.uuid4())
        #     new_uid = ''.join(uid.split('-'))
        #     status = 0
        #     if test_info["status"] == "成功":
        #         status = 0
        #     elif test_info["status"] == "失败":
        #         status = 1
        #     elif test_info["status"] == "错误":
        #         status = 2
        #     elif test_info["status"] == "跳过":
        #         status = 3
        #     test_log = ""
        #     for test_info_log in test_info["log"]:
        #         test_log += test_info_log.replace("'", "\\'")
        #     # 转换时长
        #     run_duration = float(test_info["spendTime"].replace("s", ""))
        #     sql = "INSERT INTO phone_service_report(`uuid`,`service_uuid`, `case_uuid`, `class_name`, `method_name`, `description`, `run_duration`, `status`, `output`, `create_time`) VALUES ('{}','{}','{}','{}','{}','{}','{}',{},'{}',NOW())".format(
        #         new_uid, param["service_uuid"], param["case_uuid"],
        #         test_info["className"], test_info["methodName"],
        #         test_info["description"], run_duration,
        #         status, test_log)
        #     mysql.exe(sql)
    except Exception as e:
        print("--> 错误 ", e)


def video_function_check(param):
    try:
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(TestCase)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(
                TestCase(name, param=param))
        result = MyBeautifulReport(suite)
        result.run_result_report()
    except Exception as e:
        print("--> 错误 ", e)


def phone_conference_verification(param):
    try:
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(PhoneConferenceCase)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(
                PhoneConferenceCase(name, param=param))
        result = MyBeautifulReport(suite)
        result.run_result_report()
    except Exception as e:
        print("错误 param 【{}】".format(param))
        traceback.print_exc()
        print("--> 错误 ", e)

def phone_conference_six_verification(param):
    try:
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(PhoneConferenceSixCase)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(
                PhoneConferenceSixCase(name, param=param))
        result = MyBeautifulReport(suite)
        result.run_result_report()
    except Exception as e:
        print("错误 param 【{}】".format(param))
        traceback.print_exc()
        print("--> 错误 ", e)
