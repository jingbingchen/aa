from base_devices import baseDevices
from base_logging import log

from tools.dm_pool import dmPool


class DeviceDM(object):

    def __init__(self):
        """
        初始化
        """

    def call_answer(self, ip):
        log.info("终端[{}]注册接听事件", ip)
        d = baseDevices.custom_device(ip)
        d.watcher.reset()
        dmPool.add_task(self.__add_pool, d)

    
    def __add_pool(self, d):
        d.watcher("answer").when('//*[@resource-id="com.android.pzPhone:id/btn_phone_activity_answer"]').click()
        d.watcher.start()


deviceDM = DeviceDM()