from datetime import datetime
import os
from pathlib import Path
import uiautomator2 as u2

from base_logging import log
from tools.dm_pool import dmPool

__devices_ip_list = []
__devices_list = []


def device_log(ip, port=None):
    """
    添加设备
    :param port: 端口
    :param ip: IP
    :return: device
    """
    log.info("自定义设备，ip:{}，端口:{}", ip, port)
    if ip not in __devices_ip_list:
        d = u2.connect(ip)  # connect to device
        __devices_list.append(d)
        __devices_ip_list.append(ip)
        logcat = DeviceLogcat()
        dmPool.add_task(logcat.read_logcat, d)
        dmPool.add_task(logcat.read_error_logcat, d)
        return d
    else:
        log.info("设备已存在提供现有设备")
        return __devices_list[__devices_ip_list.index(ip)]


class DeviceLogcat(object):

    def read_logcat(self, d):
        # 判断log文件是否存在
        if "log" not in os.listdir("./"):
            os.makedirs("log")
        # 生成文件目录
        file_path = "./log" + "/" + d.serial
        dir_name = Path(file_path)
        # 判断当前文件目录是否存在 如果不存在就创建
        if not dir_name.exists():
            os.makedirs(dir_name)
        # 打开文件
        fd, file_name = self.open_file(file_path)

        r = d.shell("logcat -v time", stream=True)
        try:
            # 读取每一行
            for line in r.iter_lines():
                # print(line.decode('utf-8'))
                fd.writelines(str(line) + "\n")
                # 获得文件大小
                file_size = (os.path.getsize(file_name) / 1024 / 1024)
                # 判断文件大小是否 需要切换文件
                if file_size > 50:
                    fd.close()
                    log.info(".| 文件内容超过50M 创建新的文件夹")
                    fd, file_name = self.open_file(file_path)
        except Exception as ex:
            log.error("[DeviceLogcat.read_logcat]异常[{}]", ex)
        finally:
            fd.close()
            # 发生异常关闭当前
            r.close()
            log.error("[{}]终端日志断开", d.serial)

    def read_error_logcat(self, d):
        # 判断log文件是否存在
        if "log" not in os.listdir("./"):
            os.makedirs("log")
        # 生成文件目录
        file_path = "./log" + "/" + d.serial + "/error"
        dir_name = Path(file_path)
        # 判断当前文件目录是否存在 如果不存在就创建
        if not dir_name.exists():
            os.makedirs(dir_name)
        # 打开文件
        fd, file_name = self.open_file(file_path)
        r = d.shell("logcat -v time *:E", stream=True)
        try:
            # 读取每一行
            for line in r.iter_lines():
                # print(line.decode('utf-8'))
                fd.writelines(str(line) + "\n")
                # 获得文件大小
                file_size = (os.path.getsize(file_name) / 1024 / 1024)
                # 判断文件大小是否 需要切换文件
                if file_size > 50:
                    fd.close()
                    log.info(".| 文件内容超过50M 创建新的文件夹")
                    fd, file_name = self.open_file(file_path)
        except Exception as ex:
            log.error("[DeviceLogcat.read_logcat]异常[{}]", ex)
        finally:
            fd.close()
            # 发生异常关闭当前
            r.close()
            log.error("[{}]终端日志断开", d.serial)

    # 打开文件
    def open_file(self, file_path):
        file_name = file_path + "/" + self.create_file_name() + ".log"
        fd = open(file_name, mode="w", encoding="utf-8")
        return fd, file_name

    # 生成文件名
    def create_file_name(self):
        file_name = datetime.now().strftime('%Y%m%d%H%M%S')
        return file_name
