import uiautomator2 as u2
from base_logging import log


class BaseDevices(object):
    """
    初始化终端设备，用户TestCase使用终端
    """
    __devices_list = []
    __devices_ip_list = []
    def_ip_list = []

    def __init__(self):
        """
        初始化
        """
        log.info("设备初始化中......")
        for i in self.def_ip_list:
            d = u2.connect(i)  # connect to device

            self.__devices_list.append(d)
            self.__devices_ip_list.append(i)

    def get_device(self, ip):
        """
        获取设备
        :param ip: ip
        :return: device
        """
        log.info("获取设备[{}]", ip)
        return self.__devices_list[self.__devices_ip_list.index(ip)]

    def custom_device(self, ip, port=None):
        """
        添加设备
        :param port: 端口
        :param ip: IP
        :return: device
        """
        log.info("自定义设备，ip:{}，端口:{}", ip, port)
        if ip not in self.__devices_ip_list:
            d = u2.connect(ip)
            # connect to device
            d.shell("tinymix \"PCM Volume\" 0")
            self.__devices_list.append(d)
            self.__devices_ip_list.append(ip)
            return d
        else:
            log.info("设备已存在提供现有设备")
            return self.__devices_list[self.__devices_ip_list.index(ip)]


baseDevices = BaseDevices()
