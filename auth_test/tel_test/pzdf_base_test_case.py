import unittest
from base_devices import baseDevices
from base_logging import log


class PzdfBaseTestCase(unittest.TestCase):

    param = None

    def __init__(self, methodName='runTest', param=None):
        super(PzdfBaseTestCase, self).__init__(methodName)
        PzdfBaseTestCase.param = param

    # @staticmethod
    # def parametrize(testcase_klass, param=None):
    #     """ Create a suite containing all tests taken from the given
    #      subclass, passing them the parameter 'param'.
    #     """
    #     testloader = unittest.TestLoader()
    #     testnames = testloader.getTestCaseNames(testcase_klass)
    #     suite = unittest.TestSuite()
    #     for name in testnames:
    #         suite.addTest(testcase_klass(name, param=param))
    #     return suite

    @classmethod
    def setUpClass(cls):
        log.info("测试开始......[{}]", cls.param)

    @classmethod
    def tearDownClass(cls):
        log.info("测试结束......[{}]", cls.param)

    def get_device(self, ip):
        return baseDevices.get_device(ip)

    def custom_device(self, ip, port=None):
        return baseDevices.custom_device(ip)
